# 定义了一些常用的文件工具类

# 写入指定位置的文件
import json


def write_file(file_path, content, mode="w"):
    with open(file_path, mode) as f:
        f.write(str(content))


def read_json(file_path):
    with open(file_path, "r") as f:
        data = json.loads(f.read().replace("\"", "").replace("\'", "\""))
        return data
