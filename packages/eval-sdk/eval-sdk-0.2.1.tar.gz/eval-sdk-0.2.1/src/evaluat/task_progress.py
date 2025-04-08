from data_deal_util import del_str_cache, incr_float, set_str_cache
import logging
from const import EXPIRE_1_HOUR, EXPIRE_24_HOUR, PROGRESS_KEY


class TaskProgress:
    """
        # 任务进度
    """

    def __init__(self, task_id, dataset_count):
        self.task_id = task_id
        self.dataset_count = dataset_count
        # 当前步骤
        self.step = -1
        self.total_progress = 0
        # 所有步骤及对应的百分比
        self.progress_percent = [
            ('完成单数据集初始化', 20 / self.dataset_count),
            ('完成单数据集下载', 50 / self.dataset_count),
            ('完成单数据集评价', 30 / self.dataset_count)]

        logging.info(
            f"任务进度初始化，任务ID：{self.task_id}，数据集数量：{self.dataset_count}，每数据集进度：{self.progress_percent}%")

        # 失败步骤及百分比
        self.fail_step = [('任务失败', -1)]

    def step_progress_4_one_dataset(self):
        """
            # 子步骤进度，该方法会自动计算当前累计进度，同时不会执行最后一步
        """

        # 当前步骤
        self.step += 1
        # 最后一步不允许通过该方法执行
        if self.step >= len(self.progress_percent):
            self.step -= 1
            return

        # if self.step == 0 and self.total_progress == 0:
        #     del_str_cache(f'{PROGRESS_KEY}{self.task_id}')

        logging.info(f"步骤：{self.progress_percent[self.step][0]}，进度：{self.progress_percent[self.step][1]}%")
        # 更新进度
        incr_float(f'{PROGRESS_KEY}{self.task_id}', self.progress_percent[self.step][1], EXPIRE_24_HOUR)

        # 当前累计进度
        self.total_progress += self.progress_percent[self.step][1]

    def finish_progress_4_one_dataset(self):
        if self.step >= (len(self.progress_percent) - 1) or self.total_progress >= 100:
            return

        # 当前步骤
        self.step += 1
        # 一次性走完到当前数据集进度
        left_progress = self.get_left_progress(self.step)

        if left_progress <= 0:
            return

        self.total_progress += left_progress

        logging.info(f"步骤：{self.progress_percent[self.step][0]}，进度：{left_progress}%")
        # 更新进度
        incr_float(f'{PROGRESS_KEY}{self.task_id}', left_progress, EXPIRE_1_HOUR)

        # 开启下一个任务进度
        self.step = -1

    def fail_progress(self):
        logging.info(f"步骤：{self.fail_step[0]}，进度：{self.fail_step[0][1]}%")
        # 更新进度
        set_str_cache(f'{PROGRESS_KEY}{self.task_id}', self.fail_step[0][1], EXPIRE_1_HOUR)

    def get_left_progress(self, step):
        """
            # 获取指定步骤之后的累计进度
        """
        # 假设我们从索引1开始遍历（即'完成评价数据下载'）
        start_index = step

        # 初始化累加值为0
        cumulative_percent = 0

        # 从指定的索引开始遍历
        for index, (task, percent) in enumerate(self.progress_percent[start_index:]):
            # 累加百分比
            cumulative_percent += percent

        return cumulative_percent
