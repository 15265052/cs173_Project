# 定义了一些常用的文件工具类

# 写入指定位置的文件
def write_file(file_path, content, mode="w"):
    with open(file_path, mode) as f:
        f.write(str(content))
