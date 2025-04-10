import os
import re

import numpy as np
import pandas as pd
import wandb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, \
    classification_report


# 读取txt内两个不同表格的数据，并将结果转换为字典列表输出
def read_multi_table_txt(file_path):
    # 读取原始内容
    with open(file_path, 'r') as f:
        content = f.read()

    # 按表格标题分割内容（假设每个新表格以"epoch"开头）
    table_blocks = re.split(r'\n(?=epoch\s)', content.strip())

    # 处理每个表格块
    table_dicts = []
    for block in table_blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]

        # 解析列名（处理制表符和混合空格）
        columns = re.split(r'\s{2,}|\t', lines[0])

        # 解析数据行（处理混合分隔符）
        data = []
        for line in lines[1:]:
            # 使用正则表达式分割多个连续空格/制表符
            row = re.split(r'\s{2,}|\t', line)
            data.append(row)

        # 创建DataFrame并自动转换数值类型
        df = pd.DataFrame(data, columns=columns)
        df = df.apply(pd.to_numeric, errors='coerce')  # 自动识别数值列，非数值转换为NaN

        # 将DataFrame转换为字典，每列以列表形式保存
        table_dict = df.to_dict(orient='list')
        table_dicts.append(table_dict)

    return table_dicts


# val和test时的相关结果指标计算
def calculate_results(all_labels, all_predictions, classes, average='macro'):
    results = {
        'accuracy': accuracy_score(y_true=all_labels, y_pred=all_predictions),
        'precision': precision_score(y_true=all_labels, y_pred=all_predictions, average=average),
        'recall': recall_score(y_true=all_labels, y_pred=all_predictions, average=average),
        'f1_score': f1_score(y_true=all_labels, y_pred=all_predictions, average=average),
        'cm': confusion_matrix(y_true=all_labels, y_pred=all_predictions, labels=np.arange(len(classes)))
    }
    return results


def calculate_metric(all_labels, all_predictions, classes, class_metric=False, average='macro avg'):
    metric = classification_report(y_true=all_labels, y_pred=all_predictions,
                                   target_names=classes, digits=4, output_dict=True)
    if not class_metric:
        metric = {
            'accuracy': metric.get('accuracy'),
            'precision': metric.get(average).get('precision'),
            'recall': metric.get(average).get('recall'),
            'f1-score': metric.get(average).get('f1-score'),
        }
        return metric
    else:
        return metric


def append_metrics(metrics, metric, result, lr):
    metrics['train_losses'].append(result['train_loss'])
    metrics['val_losses'].append(result['val_loss'])
    metrics['accuracies'].append(metric['accuracy'])
    metrics['precisions'].append(metric['precision'])
    metrics['recalls'].append(metric['recall'])
    metrics['f1-scores'].append(metric['f1-score'])
    metrics['lrs'].append(lr)
    return metrics


def initialize_results_file(results_file, result_info):
    """
    初始化结果文件，确保文件存在且第一行包含指定的内容。

    参数:
        results_file (str): 结果文件的路径。
        result_info (list): 需要写入的第一行内容列表。
        space:列名间隔（默认两个空格的距离）
    """
    # 处理 result_info，在每个单词后添加两个空格
    result_info_str = '  '.join(result_info) + '\n'
    # 检查文件是否存在
    if os.path.exists(results_file):
        # 如果文件存在，读取第一行
        with open(results_file, "r") as f:
            first_line = f.readline().strip()
        # 检查第一行是否与 result_info 一致
        if first_line == result_info_str.strip():
            print(f"文件 {results_file} 已存在且第一行已包含 result_info，不进行写入。")
        else:
            # 如果不一致，写入 result_info
            with open(results_file, "w") as f:
                f.write(result_info_str)
            print(f"文件 {results_file} 已被重新初始化。")
    else:
        # 如果文件不存在，创建并写入 result_info
        with open(results_file, "w") as f:
            f.write(result_info_str)
        print(f"文件 {results_file} 已创建并写入 result_info。")


def is_similar_key(key1, key2):
    """
    检查两个键是否相似，考虑复数形式的转换。

    Args:
        key1 (str): 第一个键
        key2 (str): 第二个键

    Returns:
        bool: 如果两个键相似（包括复数形式的转换），返回 True，否则返回 False
    """
    if key1 == key2:
        return True

    # 检查 key2 是否是复数形式
    if key2.endswith("ies"):
        singular_candidate = key2.removesuffix("ies") + "y"
        if key1 == singular_candidate:
            return True

    if key2.endswith("es"):
        singular_candidate = key2.removesuffix("es")
        if key1 == singular_candidate:
            return True

    if key2.endswith("s"):
        singular_candidate = key2.removesuffix("s")
        if key1 == singular_candidate:
            return True

    return False


def append_to_results_file(file_path: str,
                           data_dict: dict,
                           column_order: list,
                           float_precision: int = 4,
                           more_float: int = 2,
                           custom_column_widths: dict = None) -> None:
    """
    通用格式化文本行写入函数

    参数：
    file_path: 目标文件路径
    data_dict: 包含数据的字典，键为列名
    column_order: 列顺序列表，元素为字典键
    float_precision: 浮点数精度位数 (默认5位)
    more_float: 额外的浮点数精度位数
    custom_column_widths: 自定义列宽的字典，键为列名，值为列宽
    """
    # 计算每列的最大宽度
    column_widths = []
    formatted_data = []
    for col in column_order:
        # 查找 data_dict 中相似的键
        dict_key = None
        for key in data_dict:
            if is_similar_key(key, col):
                dict_key = key
                break
        if dict_key is None:
            raise ValueError(f"Missing required column: {col}")

        value = data_dict[dict_key]

        # 根据数据类型进行格式化
        if isinstance(value, (int, np.integer)):
            fmt_value = f"{value:d}"
        elif isinstance(value, (float, np.floating)):
            if col in ['train_losses', 'val_losses']:  # 如果列名是'train_losses'或'val_losses'，保留浮点数精度位数+1位
                fmt_value = f"{value:.{float_precision + more_float}f}"
            elif col == 'lrs':  # 如果列名是'lrs'，保留8位小数
                fmt_value = f"{value:.8f}"
            else:
                fmt_value = f"{value:.{float_precision}f}"
        elif isinstance(value, str):
            fmt_value = value
        else:  # 处理其他类型转换为字符串
            fmt_value = str(value)

        # 确定列宽
        if custom_column_widths and col in custom_column_widths:
            column_width = custom_column_widths[col]
        else:
            # 取列名长度和数值长度的最大值作为列宽
            column_width = max(len(col), len(fmt_value))
        column_widths.append(column_width)

        # 应用列宽对齐
        if col == column_order[-1]:  # 最后一列左边对齐
            fmt_value = fmt_value.ljust(column_width)
        else:
            fmt_value = fmt_value.rjust(column_width)

        formatted_data.append(fmt_value)

    # 构建文本行并写入，列之间用两个空格分隔
    line = "  ".join(formatted_data) + '\n'
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(line)


def get_wandb_key(key_path):
    with open(key_path, 'r', encoding='utf-8') as f:
        key = f.read()
    return key


def wandb_init(project=None, key_path=None, name=None):
    run = None
    if project is not None:
        if key_path is None:
            raise ValueError("When 'project' is not None, 'key_path' should also not be None.")
        wandb_key = get_wandb_key(key_path)
        wandb.login(key=wandb_key)
        run = wandb.init(project=project, name=name)
    return run


def list_folders(path):
    # 获取目录下的所有内容
    entries = os.listdir(path)
    # 筛选只保留文件夹
    folders = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    return folders
