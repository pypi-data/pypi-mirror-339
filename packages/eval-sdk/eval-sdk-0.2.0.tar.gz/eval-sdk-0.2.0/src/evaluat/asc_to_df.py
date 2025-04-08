import pandas as pd
from collections import defaultdict
import cantools
from can import ASCReader

def read_raw_asc_to_dataframe(source_file, protocol_file):
    """
    从ASC文件读取原始CAN数据并转换为DataFrame（不进行插值处理）

    参数:
        source_file: ASC文件路径
        protocol_file: DBC协议文件路径

    返回:
        df: 包含原始CAN数据的DataFrame（保留原始时间戳）
        error_messages: 错误信息列表
    """
    # 初始化变量
    data_records = []
    message_counts = defaultdict(int)

    # 加载DBC文件
    db = cantools.db.load_file(protocol_file)

    # 读取ASC文件
    asc = ASCReader(source_file, relative_timestamp=False)

    # 核心解析逻辑
    for msg in asc:
        if msg.arbitration_id not in db._frame_id_to_message:
            continue

        frame = db._frame_id_to_message[msg.arbitration_id]
        message = frame.decode(msg.data, False)
        message['timestamp'] = msg.timestamp
        message['message_name'] = frame.name
        message_counts[frame.name] += 1

        # 将信号展平为记录
        record = {'timestamp': msg.timestamp}
        for signal_name, value in message.items():
            if signal_name in ['timestamp', 'message_name']:
                continue
            record[f"{frame.name}.{signal_name}"] = value

        data_records.append(record)

    # 转换为DataFrame
    if data_records:
        df = pd.DataFrame(data_records)
        df.set_index('timestamp', inplace=True)
        df.index.name = 'timestamp'

        # 打印消息统计信息
        print("\n消息统计:")
        for msg, count in message_counts.items():
            print(f"{msg}: {count} 条")
    else:
        df = pd.DataFrame()

    return df


def print_first_100_rows(df):
    """
    精确打印DataFrame前100行，保持整齐的列对齐格式

    参数:
        df: 输入的CAN数据DataFrame
    """
    # 确保有timestamp索引
    if df.index.name != 'timestamp':
        df = df.reset_index().set_index('timestamp')

    # 只取前100行
    df_subset = df.head(100)

    # 计算各列最大宽度（最小20字符）
    col_widths = {
        'timestamp': 20,
        ** {col: max(20, len(col) + 2) for col in df.columns}
    }

    # 打印表头
    header = "timestamp".ljust(col_widths['timestamp'])
    for col in df.columns:
        header += col.rjust(col_widths[col])
    print(header)

    # 打印分隔线
    separator = '-' * col_widths['timestamp']
    for col in df.columns:
        separator += '-' * col_widths[col]
    print(separator)

    # 打印数据行
    for ts, row in df_subset.iterrows():
        # 格式化时间戳（保留6位小数）
        line = f"{ts:.6f}".ljust(col_widths['timestamp'])

        # 格式化每个信号值
        for col, value in row.items():
            if pd.isna(value):
                cell = "NaN"
            elif isinstance(value, bool):
                cell = str(value)
            elif isinstance(value, (int, float)):
                cell = f"{float(value):.1f}" if value % 1 else f"{int(value)}"
            else:
                cell = str(value)

            line += cell.rjust(col_widths[col])

            # dict
            # signal1-key : list<timestamp signal1-value>
            # signal1-key: list<timestamp signal2 >
            # timestamp signal3
            #
            # 123
            # getmsg("acan", msgid, signalname)

        print(line)


# 使用示例
if __name__ == '__main__':
    df = read_raw_asc_to_dataframe("./ACAN_2_20241112160934.asc", "./ACAN.dbc")
    print_first_100_rows(df)
