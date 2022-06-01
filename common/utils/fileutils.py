# 定义了一些常用的文件工具类

# 写入指定位置的文件
import json
import pandas as pd

def write_file(file_path, content, mode="w"):
    with open(file_path, mode, encoding='utf-8') as f:
        f.write(str(content))


def read_json(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        data = json.loads(f.read().replace("\"", "").replace("\'", "\""))
        return data

def read_csv(file_path):
    return pd.read_csv(file_path)