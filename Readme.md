# 代码文件描述
# common 
通用模块
# utils/fileutils.py
该文件包含了一些读取写入文件的操作，有：
- write_file: 将内容写入指定文件
- read_json: 读入指定json格式文件
- read_csv: 读入指定csv格式文件，以pandas的DataFrame格式返回
# DataCrawl
数据爬取模块
## config/apis.py
该文件包含了一系列获取数据的api接口host
## request.py
该文件封装了一系列调取api的函数
## mainCrawl.py
该文件是爬取数据模块的入口函数，首先单线程模式下爬取了中国所有迄今为
止的新冠疫情各方面的数据汇总，后由于获取各病例的详情信息时，一个病例
就需要调用一次api，所以采取了多线程的模式，并发请求接口，获取所有api
提供的病例详情

# DataClean
数据清洗模块
## cleanChinaDaily.py
将数据爬取模块中爬取到的中国日增数据从json字典格式转换成pandas的表格形式，并清洗掉无用信息
## cleanProvinceDaily.py
将数据爬取模块中爬取到的中国各省份日增数据从一个文件中抽离出来，清除掉无用数据之后，按省份分为不同文件，以表格形式存储
## cleanSpecificInfo.py
将数据爬取模块中爬取到的所有病例详细信息清洗掉无用信息后，从json字典格式转换成pandas的表格形式存储

# DataAnalyse
数据分析模块
## config
### amapApi.py
该文件包含了高德地图的api接口host
### constants.py
该文件包含了调用高德地图关键字查询所需要的用户key
## markPos
### markMain.py
该文件采用多线程的方式，并发调用高德地图关键字查询的接口，查询病例所在地点的类型，添加到原数据新增一栏地点类型中。
## process
### classify.py
该文件将聚类得到的结果按照cluster来分成不同文件

# Model1
# Model2
# Model3
gru模型
## main.ipynb
该文件包含所有gru模型相关代码，包括预处理、调参、训练、结果评估
## result.md
该文件包含调参结果和3种模型对3类数据的预测结果
## Preformance Evaluation.png
该文件为结果评估可视化
## word_embedding.py
## deprecated.py
该文件为曾使用过的代码存档