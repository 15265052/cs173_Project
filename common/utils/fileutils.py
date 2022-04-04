# 定义了一些常用的文件工具类
import os
# 写入指定位置的文件
def write_file(file_path, content, mode="w"):

    if not os.path.exists("".join(file_path.split("/")[:-1])):
        os.makedirs("".join(file_path.split("/")[:-1]))

    with open(file_path, mode) as f:
        f.write(str(content))
