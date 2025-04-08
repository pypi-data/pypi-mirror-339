import sys
import base64
from operator_framework import OperatorFramework
import logging
from util import nacos_client
import json
from evaluat import db_util
from const import SOURCE, LOGSIM, SCENE, SUCCESS, FAILED, EXECUTE, ERROR, STR_FAIL, STR_PASS, STR_ERROR
from evaluat.source_data_init_strategy import SourceDatasetInitStrategy
from evaluat.logsim_data_init_strategy import LogsimDatasetInitStrategy
from evaluat.sence_data_init_strategy import SenceDatasetInitStrategy
import const_key
import data_deal_util
import scene_util
from evaluat import data_util
from evaluat.task_progress import TaskProgress
import traceback
from redis_util import RedisDistributedLock
import es_util
import pandas as pd
import os
import shutil
import label_util
from util.redis_module import redis_client
from log_manager import LoggingManager
from collections import defaultdict

strategy_dict = {
    LOGSIM: LogsimDatasetInitStrategy(),
    SCENE: SenceDatasetInitStrategy(),
    SOURCE: SourceDatasetInitStrategy()}

lock_name_prefix = 'eval:task:'

# 评价任务id
task_id_g = None

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()


def main():
    """
    入口函数：
        1.数据初始化
        2.创建任务
        3.加载、执行算子
    """

    logging.info(sys.argv)

    if len(sys.argv) < 3:
        logging.info("Please provide arguments.")
        raise Exception("参数错误")

    # 页面参数
    param_page = sys.argv[1]
    param_page = json.loads(param_page)
    logging.info("页面参数为：{}".format(param_page))
    # 上游传递参数
    param_pipeline = sys.argv[2]
    param_pipeline = json.loads(param_pipeline)
    logging.info("传递参数：{}".format(param_pipeline))

    # 1 源数据 2 数据集
    source_type = int(param_pipeline['source_type'])
    # 逗号分隔的数据集id
    source_id_list = param_pipeline['source_id_list']

    # 初始化任务
    bc_name = param_page["bc_name"]
    op_file_name = param_page["op_file_name"]
    config_str = param_page["config_str"]

    metric_config = base64.b64decode(param_page['metric_config']).decode('utf-8')
    op_strs = param_page['op_strs']
    common_strs = param_page['common_strs']


    # 从git中拉取算子代码及对应配置
    metric_config_json = json.loads(metric_config)
    script_local_path_list = data_deal_util.generate_local_op_file(op_strs)
    # 保存common函数脚本文件，用于后续算子调用
    data_deal_util.generate_local_op_file(common_strs)

    if not script_local_path_list:
        raise Exception("下载算子文件失败")
    # 加载算子
    operator_framework = OperatorFramework()
    operator_framework.load_multiple_operators(script_local_path_list)

    # 执行算子
    # 初始化任务
    task_id = init_task(bc_name, op_file_name, config_str, param_page, param_pipeline)
    global task_id_g
    task_id_g = task_id

    # 初始化评价任务及其数据集
    init_task_dataset(task_id, source_id_list, source_type)

    # 获取任务需要处理的数据集
    task_dataset_list = db_util.get_evluate_task_dataset(task_id)

    execute_operator(task_id, operator_framework, param_page, param_pipeline,
                     script_local_path_list, metric_config_json, task_dataset_list)

    # 更新任务
    db_util.update_task_4_success(task_id)

    # 输出参数到下一个节点
    param_pipeline_next = {'task_id': task_id, 'node_name': "评测任务"}
    param_pipeline_next = json.dumps(param_pipeline_next)
    # 写入回灌流水线中间数据到下一个节点
    with open('./outParams.txt', 'w', encoding='utf-8') as file:
        file.write(param_pipeline_next)


def save_middle_files(operators_cvs_df_list, operators_topic_df_list, task_dataset_id, dataset_id):
    # 合并所有 cvs_df
    if operators_cvs_df_list:
        operators_cvs_df = pd.concat(operators_cvs_df_list, ignore_index=True)  # 合并所有 DataFrame
        # 保存到本地 CSV 文件
        dataset_csv_path = os.path.join(const_key.LOCAL_RESULT_PREFIX, "analysis.csv")
        operators_cvs_df.to_csv(dataset_csv_path, index=False)  # 保存为 CSV，不包括行索引
        LoggingManager.logging().info("analysis.csv has been saved ")
    else:
        LoggingManager.logging().info("No analysis.csv to save ")

    # 如果你需要处理 operators_topic_df_list，可以在这里添加类似的逻辑
    # 例如：
    if operators_topic_df_list:
        operators_topic_df = pd.concat(operators_topic_df_list, ignore_index=True)
        dataset_topic_path = os.path.join(const_key.LOCAL_RESULT_PREFIX, "topic.csv")
        operators_topic_df.to_csv(dataset_topic_path, index=False)
        LoggingManager.logging().info("topic.csv has been saved")
    else:
        LoggingManager.logging().info("No topic.csv to save")

    # 上传文件
    package_log_file = str(dataset_id)+".log"
    file_names = ["analysis.csv", "topic.csv", package_log_file]  # scene_util.list_file_names(const.LOCAL_RESULT_PREFIX)
    obs_dir = "datacenter_result/eval/" + str(task_dataset_id) + "/"
    LoggingManager.logging().info(f"中间文件上传到: {obs_dir}")

    # 管理日志记录器
    LoggingManager.release_logger()
    # data_deal_util.close_logger_handler(cus_logging)

    # /a/b/a.txt /a/b/c.txt
    result_local_file = []
    result_local_file_name = []
    # 云完整路径
    result_obs_path = []

    for file_name in file_names:
        # 统一上传后的日志文件
        result_obs_file = obs_dir + ("log.log" if file_name == package_log_file else file_name)
        # 上传回灌结果
        file_path = os.path.join(const_key.LOCAL_RESULT_PREFIX, file_name)
        if not os.path.isfile(file_path):
            logging.info(f"File {file_path} does not exist.")
            continue

        result_local_file_name.append("log.log" if file_name == package_log_file else file_name)
        result_local_file.append(file_path)
        data_deal_util.upload_to_obs(result_obs_file, file_path)

        result_obs_path.append(result_obs_file)
        logging.info(f"评价中间文件{file_path}保存到OBS {result_obs_file}")

    if result_local_file_name:
        # 更新文件地址
        db_util.update_evluate_task_dataset_middle_files(task_dataset_id, ",".join(map(str, result_local_file_name)))

        # 删除临时文件：结果文件
        scene_util.remove_files(result_local_file)

    return result_obs_path


def save_label(operator_result_dict, params):
    """
    保存评测标签
    @param operator_result_dict: 每个算子的结果 key 算子名称，value 算子结果
    """
    task_dataset = params[const_key.KEY_TASK_DATASET]
    task_info = db_util.get_evaluate_task(task_dataset["task_id"])[0]
    main_task_info = db_util.get_evaluate_main_tas_by_id(task_info["parent_task_id"])[0]

    # 评测算子处理的数据包信息
    dataset_label_dict = params[const_key.DATASET_LABEL_KEY]
    # 保存评测标签
    evaluate_info_label = {"create_time": main_task_info["create_time"].timestamp() * 1000,
                           "creator": main_task_info["creater"],
                           "id": task_dataset["id"],
                           "task_id": main_task_info["id"],
                           "task_name": main_task_info["task_name"]}

    # 所有算子结果
    # 记录每一个算子名（key）和该算子结果（value:pass\fail)，同是汇总所有算子结果(key:reslut value:pass/fail)，作为数据包的处理结果
    operator_pass_dict = {}
    if operator_result_dict:
        for operator_name, operator_result in operator_result_dict.items():
            if not operator_result:
                continue

            # 检查 operator_data 是字典（对应 JSONObject）还是列表（对应 JSONArray）
            if isinstance(operator_result, dict):
                # 获取 'result' 字段的值
                result = operator_result.get("result")
                # 将算子结果名称和 result 值存入字典
                operator_pass_dict[operator_name] = result.strip() if result else STR_ERROR
            elif isinstance(operator_result, list):
                # 遍历所有结果，都为 "pass" 才认为通过
                pass_value = None
                for item in operator_result:
                    if not isinstance(item, dict):
                        continue
                    result_str = item.get("result")
                    result_str = result_str.strip() if result_str else STR_ERROR
                    # 有一个失败表示本次算子失败
                    if result_str == STR_ERROR:
                        pass_value = STR_ERROR
                        break

                    if result_str == STR_FAIL:
                        pass_value = STR_FAIL
                        break
                    pass_value = result_str
                operator_pass_dict[operator_name] = pass_value
            else:
                operator_pass_dict[operator_name] = STR_ERROR

    # 汇总所有算子结果
    # total_result = STR_FAIL if any(value == STR_FAIL for value in operator_pass_dict.values()) else STR_PASS

    values = operator_pass_dict.values()
    if any(value == STR_ERROR for value in values):
        total_result = STR_ERROR
    elif any(value == STR_FAIL for value in values):
        total_result = STR_FAIL
    else:
        total_result = STR_PASS

    operator_pass_dict["result"] = total_result

    evaluate_info_label["operator_result"] = operator_pass_dict

    dataset_label_dict["evaluate_info"] = evaluate_info_label

    LoggingManager.logging().info(f"保存评测标签：{dataset_label_dict}")
    label_util.saveEvaluateDataLabel(task_dataset["id"], dataset_label_dict)
    pass

def save_result(operator_name: str, operator_result: dict, metric_config:dict, params: dict,
                table_name: str, dataset_label: dict) -> None:
    """
    将算子结果保存到ES
    @param operator_name: 算子名称
    @param operator_result: 算子结果
    @param params: 算子参数
    @param table_name: 算子结果保存的表名
    """

    # 确保有结果返回
    if not operator_result:
        LoggingManager.logging().info(f"算子 {operator_name} 结果是 None or empty.")
        return

    # 算子任务需要处理的数据集
    task_dataset = params[const_key.KEY_TASK_DATASET]
    # 获取公共数据信息，如：天气，白天等信息
    dataset_info, operator_info = data_util.get_common_data(params, task_dataset)

    operator_info["metric_config"] = metric_config
    operator_info["operator_name"] = operator_name

    # 获取任务信息
    task_info = db_util.get_evaluate_task(task_dataset["task_id"])[0]
    task_info_dict = {"task_id": task_info["parent_task_id"],
                      "son_task_id": task_info["id"],
                      "batch_no": task_info["batch_no"],
                      "op_file_name": task_info["op_file_name"],
                      "bc_name": task_info["bc_name"],
                      "config_str": task_info["config_str"]}

    # 保存结果到ES：每隔一个segment保存一条记录
    # 判断 operator_result 的类型并根据不同类型进行处理
    if isinstance(operator_result, dict):
        # 如果是 dict 类型，进行相关处理
        LoggingManager.logging().info("处理 operator_result dict 类型的数据")
        save(dataset_info, operator_name, operator_result, task_info_dict, operator_info, dataset_label, table_name)
    elif isinstance(operator_result, list) and len(operator_result) > 0:
        # 如果是 list 类型，进行相关处理
        LoggingManager.logging().info("处理 operator_result list 类型的数据")
        for item in operator_result:
            save(dataset_info, operator_name, item, task_info_dict, operator_info, dataset_label, table_name)
    else:
        # 如果不是 dict 或 list，可能是错误或其他类型，可以抛出异常或做默认处理
        LoggingManager.logging().info("operator_result 结果类型未知或空列表")


def save(dataset_info, operator_name, operator_result, task_info, operator_info, dataset_label, table_name):
    if "start_timestamp" in dataset_info:
        start_timestamp = dataset_info["start_timestamp"]
    else:
        start_timestamp = 0

    if "end_timestamp" in dataset_info:
        end_timestamp = dataset_info["end_timestamp"]
    else:
        end_timestamp = 0

    dataset_info["playback_url"] = data_util.gen_playback_url(start_timestamp, end_timestamp,
                                                              dataset_info["task_dataset_id"])

    # # 处理约定通用结果列，存放结果
    # common_result = {}
    # if "result" in operator_result:
    #     common_result["result"] = operator_result["result"]
    # if "event_timestamp" in operator_result:
    #     common_result["event_timestamp"] = operator_result["event_timestamp"]



    operator_info = {operator_name: operator_info}
    # 构建结果字典
    operator_name_result = {operator_name: operator_result}
    result = {"operator_result": operator_name_result, "task_info": task_info,
              "dataset_info": dataset_info, "operator_name": operator_name, "operator_info": operator_info}

    # 把标签值添加到结果中
    # 标签只入库部分数据
    #label_dict = {"basic_info": dataset_label["basic_info"], "data_info": dataset_label["data_info"]}
    #result.update(label_dict)

    LoggingManager.logging().info(f"算子 {operator_name} 结果表 {table_name}：结果为 {result}")
    es_util.save(table_name, result)


def is_operator_success(operator_result_dict: dict):
    """
    判断所有算子结果是否全部为success
    @param operator_result_dict: 算子结果
        {"operator_a":[{result:success, ...}, {...}], "operator_b":[{result:success, ...}, {...}}]}
    """

    if operator_result_dict is None or not operator_result_dict:
        return False

    all_success = True

    # 遍历所有可能的result字段
    for key, value_list in operator_result_dict.items():
        for item in value_list:
            if 'result' not in item or item['result'] != 'pass':
                all_success = False
                break  # 如果找到一个不是success的，就可以提前退出内层循环
        if not all_success:
            break  # 同样，如果外层循环中已经确定不是所有都是success，也可以提前退出

    return all_success


def execute_operator(task_id, operator_framework, param_page, param_pipeline,
                     script_local_path_list, metric_config, task_dataset_list):
    """
    按数据集循环执行算子
    @:param task_id: 子任务ID
    """
    son_task_info = db_util.get_evaluate_task(task_id)[0]
    main_task_id = son_task_info["parent_task_id"]
    process_cache_key = f"{current_config.get('cache', {}).get('eval:process')}{main_task_id}"

    # 算子部分参数
    operator_param = {"param_page": param_page, "param_pipeline": param_pipeline}
    # 对所有数据包执行算子，每个数据包采用不同的日志文件
    for task_dataset in task_dataset_list:
        operators_cvs_df_list = None
        operators_topic_df_list = None

        dataset_id = task_dataset["dataset_id"]

        # 设置当前 package_id 并初始化 logger
        LoggingManager.set_current_package(str(dataset_id), const_key.LOCAL_RESULT_PREFIX)

        try:
            # dataset_log_path = os.path.join(const_key.LOCAL_RESULT_PREFIX, "log.log")
            # 每个数据包采用不同的日志文件
            LoggingManager.logging().info(f"准备一个数据包的评价 start:{dataset_id}")

            # 进度条
            task_progress = TaskProgress(task_id, len(task_dataset_list))

            # 进度：完成单数据初始化
            task_progress.step_progress_4_one_dataset()

            dataset_info = {"dataset_path": task_dataset["dataset_path"],
                            "start_timestamp": task_dataset["start_timestamp"],
                            "end_timestamp": task_dataset["end_timestamp"],
                            "start_frame_no": task_dataset["start_frame_no"],
                            "end_frame_no": task_dataset["end_frame_no"],
                            "tag_name": task_dataset["tag_name"]}
            operator_param[const_key.KEY_DATASET_INFO] = dataset_info

            # 下载评价数据集
            local_source_path_list, local_logsim_result_data_path_list, json_list = download_one_dataset(task_dataset)

            # 进度：完成单数据下载
            task_progress.step_progress_4_one_dataset()

            # 算子参数：评测数据本地数据集路径
            operator_param[const_key.LOCAL_CHANNEL_FILE_INDEX] = local_source_path_list
            operator_param[const_key.LOCAL_RAW_DOWNLOAD_PATH_KEY] = json_list
            operator_param[const_key.LOCAL_LOGSIM_RESULT_DOWNLOAD_PATH_KEY] = local_logsim_result_data_path_list

            # 算子要处理的数据包信息
            try:
                operator_param[const_key.DATASET_LABEL_KEY] = get_dataset_label(task_dataset["dataset_id"], task_dataset["dataset_type"])
            except Exception as e:
                LoggingManager.logging().error(f'获取数据集{task_dataset["dataset_id"]}标签失败：{e}')
                operator_param[const_key.DATASET_LABEL_KEY] = {}

            # json 算子配置信息
            operator_param[const_key.KEY_METRIC_CONFIG] = metric_config
            operator_param[const_key.KEY_TASK_DATASET] = task_dataset

            # 执行算子
            operator_result_dict, operators_cvs_df_list, operators_topic_df_list, operator_version_dict = (
                operator_framework.execute_multiple_operators(script_local_path_list, operator_param,
                                                              save_result_method=save_result))

            if operator_result_dict:
                operator_result_json = json.dumps(operator_result_dict)
            else:
                operator_result_json = None

            # 判断所有算子是否成功
            operator_is_success = is_operator_success(operator_result_dict)

            # 完成一个数据包的评测：成功
            db_util.update_evluate_task_dataset(task_dataset["id"], operator_result_json, SUCCESS if operator_is_success else FAILED)

            LoggingManager.logging().info(f"完成一个数据包的评价 end:{dataset_id}")

            # 进度：完成单数据集评价
            task_progress.finish_progress_4_one_dataset()

            # 删除上一次回灌文件，防止容器磁盘爆满
            # scene_util.remove_dirs([const.LOCAL_DIR_PREFIX])
            shutil.rmtree(const_key.EVAL_LOCAL_DIR_PREFX)
            save_label(operator_result_dict, operator_param)
            # 完成一个数据包
            redis_client.hincrement(process_cache_key, 'success' if operator_is_success else 'fail', 1)
        except Exception as err:
            save_label({"result": {"result": STR_ERROR}}, operator_param)
            LoggingManager.logging().exception("数据ID：%s，数据处理异常", task_dataset["dataset_id"])

            # 使用traceback模块来打印完整的错误栈信息
            traceback.print_exc()
            # 或者，如果你想要捕获错误信息到字符串中
            error_info = traceback.format_exc()

            LoggingManager.logging().info(
                f"Error executing operator 任务失败 Error: {err.__class__.__name__}: {err}。详细信息：{error_info}")

            redis_client.hincrement(process_cache_key, 'error', 1)
            # 完成一个数据包的评测：失败
            db_util.update_evluate_task_dataset(task_dataset["id"], None, ERROR)
        finally:
            try:
                save_middle_files(operators_cvs_df_list, operators_topic_df_list, task_dataset["id"], task_dataset["dataset_id"])
                redis_client.hincrement(process_cache_key, 'wait', -1)
            except:
                logging.exception("数据ID：%s，保存中间文件异常", task_dataset["dataset_id"])


def get_parquet_index(source_data_list):
    """
    计算每个 source_data_id 独立的时间区间，并建立：
    2. `channel_file_index`：按通道（如 pcan, acan）组织，存储相关的 parquet 文件，方便跨包合并

    确保时间段连续，返回两个索引结构。
    """
    LoggingManager.logging().info("download scene dataset")

    channel_file_index = defaultdict(list)  # 以通道为 key，存储相关的 parquet 文件

    # 按 raw_time 排序，确保顺序处理
    for row in sorted(source_data_list, key=lambda x: x['raw_time']):
        raw_time_str = row['raw_time'].strftime("%Y%m%d_%H%M%S")
        obs_prefix = f"{row['project_name']}/{row['plate_no']}/raw_{raw_time_str}/canbus/"
        local_path = data_util.get_local_path(obs_prefix)

        # 下载该包的所有 Parquet 文件
        downloaded_files = data_deal_util.download_parquet_files(obs_prefix, local_path)

        for file in downloaded_files:
            # 解析通道名称，例如 pcan_1.parquet -> pcan
            channel_key = os.path.basename(file).split("_")[0].lower()
            channel_file_index[channel_key].append(file)

    return dict(channel_file_index)


def download_by_extension(file_extension: str, source_data):
    """
    按扩展名下载包内文件
    """
    # 仅仅下载特定文件
    raw_time_str = source_data['raw_time'].strftime("%Y%m%d_%H%M%S")
    cloud_raw_path = f"{source_data['project_name']}/{source_data['plate_no']}/raw_{raw_time_str}/"
    local_raw_path = data_util.get_local_path(cloud_raw_path)
    filter_file_subfix_tuple = (file_extension)
    success, local_path_list = data_deal_util.download_folder_from_obs(cloud_raw_path, local_raw_path,
                                                                       filter_file_subfix_tuple)
    return local_path_list


def download_one_dataset(task_dataset):
    """
    下载一个评测数据集包
    """
    # 评测数据集
    # 获取到需要回灌场景数据，支持挎包
    if task_dataset["dataset_type"] == LOGSIM:  # 针对非回灌数据评价
        source_data_ids = task_dataset["source_data_ids"]
    else:
        dataset_id = task_dataset['dataset_id']
        dig_data = db_util.get_dig_data_by_id(dataset_id)
        source_data_ids = dig_data["source_data_ids"]

    # 获取到场景数据对应的原始数据列表(支持跨片挖掘回灌)
    source_data_list = db_util.get_source_data(source_data_ids)
    channel_file_index = get_parquet_index(source_data_list)

    json_list = download_by_extension(".json", source_data_list[0])

    # 下载单个回灌结果文件
    local_logsim_result_data_path_list = {}
    if task_dataset["dataset_type"] == LOGSIM:  # 针对非回灌数据评价
        LoggingManager.logging().info(f"download logsim result data")
        # 下载单个回灌结果文件
        cloud_raw_path = task_dataset["dataset_path"]
        local_raw_path = data_util.get_local_path(cloud_raw_path)
        # filter_file_subfix_tuple = (".parquet")
        success_logsim_result_data, local_logsim_result_data_path_list = data_deal_util.download_folder_from_obs(
            cloud_raw_path, local_raw_path)

        if not success_logsim_result_data:
            LoggingManager.logging().info(f"eval file download failed: {cloud_raw_path} exit")
            raise Exception("eval file download failed: {}".format(cloud_raw_path))

    return channel_file_index, local_logsim_result_data_path_list, json_list


def init_task_dataset(task_id, source_id_list, dataset_type):
    # 任务重复执行，幂等性处理
    db_util.delete_evluate_task_dataset(task_id)

    # 根据数据集类型、数据集来源类型、任务类型，初始化评价数据集
    init_data_strategy = strategy_dict[dataset_type]
    if not init_data_strategy:
        raise Exception("不支持的评价数据集类型 dataset_type:{}".format(dataset_type))

    # 获取评价数据
    # vehicle_info = get_dataset(source_id_list, dataset_type)
    init_data_strategy.parser_dataset(source_id_list, dataset_type).init_task_dataset(task_id)


def get_dataset_label(dataset_id, dataset_type):
    """
    获取到数据对应的标签
    @param 源数据表、切片表、场景表、回灌结果表 对应主键id
    """
    # 根据数据集类型、数据集来源类型、任务类型，初始化评价数据集
    init_data_strategy = strategy_dict[dataset_type]
    if not init_data_strategy:
        raise Exception("不支持的评价数据集类型 dataset_type:{}".format(dataset_type))

    return init_data_strategy.get_dataset_label(dataset_id)


# def init_task(logsim_task_id, bc_name, op_file_name, config_str, param_page, param_pipeline, metric_json):
def init_task(bc_name, op_file_name, config_str, param_page, param_pipeline):
    if "is_work_flow" in param_pipeline and param_pipeline["is_work_flow"] == 0:
        task_id = param_pipeline["eval_task_id"]
        # db_util.update_task_4_start(task_id, json.dumps(metric_json))
        db_util.update_task_4_start(task_id)
    else:
        # # 生成评价任务：工作流任务是在argo 启动容器后初始化落库
        # argo_task_name = sys.argv[3]
        # task_name = param_page["job_code"]
        # # "job_code":"j241026000001-1"
        # batch_no = param_page["job_code"].split("-")[0]
        #
        # logsim_task = None
        # if logsim_task_id is not None:
        #     logsim_task = db_util.get_logsim_task(logsim_task_id)[0]
        #
        # main_task_id = create_main_task(argo_task_name, batch_no, bc_name, config_str, logsim_task, logsim_task_id,
        #                                 op_file_name, task_name, None)  #json.dumps(metric_json))
        #
        # task_id = db_util.save_evaluate_task(logsim_task, logsim_task_id, task_name, bc_name, op_file_name,
        #                                      config_str, EXECUTE, argo_task_name, batch_no, main_task_id)
        task_id = None
    return task_id


def create_main_task(argo_task_name, batch_no, bc_name, config_str, logsim_task, logsim_task_id, op_file_name,
                     task_name, metric_json):
    #  创建批次任务：工作流任务是在argo启动容器后初始化落库
    main_task_id = None
    lock = RedisDistributedLock(lock_name_prefix + batch_no, expire=5)
    if lock.acquire(blocking=True, timeout=10):
        try:
            main_task = db_util.get_evaluate_main_task(batch_no)
            # 总任务不存在，创建
            if main_task is None or len(main_task) == 0:
                main_task_id = db_util.save_evaluate_main_task(logsim_task, logsim_task_id, task_name, bc_name,
                                                               op_file_name, config_str, EXECUTE, batch_no, metric_json)
        finally:
            lock.release()
    else:
        logging.error(f"failed to acquire lock within timeout.")

    return main_task_id


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        # 使用traceback模块来打印完整的错误栈信息
        traceback.print_exc()
        # 或者，如果你想要捕获错误信息到字符串中
        error_info = traceback.format_exc()

        logging.info(f"任务 {task_id_g} 失败 Error: '{err.__class__.__name__}: {err}'。详细信息：'{error_info}'")
        db_util.update_task_4_failed(task_id_g)

        # 步骤error：任务失败，进度key设置过期
        TaskProgress(task_id_g, 1).fail_progress()
    finally:
        shutil.rmtree(current_config.get('containerPath'))
