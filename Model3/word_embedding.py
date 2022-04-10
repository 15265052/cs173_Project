import fasttext
import pandas as pd
import json
import jieba
import numpy as np

pretrained_model = fasttext.load_model("cc.zh.300.bin.gz.download/cc.zh.300.bin")
China_data = pd.read_csv(r"/Users/a1/Desktop/数据挖掘CS173/cs173_Project/DataCrawl/RawData/marked_specific_info(1).csv")
x_length = len(China_data['time'].values)
all = []
for i in range(x_length):
    all_temp = {}
    place_type = str(China_data['place_type'][i])
    place = list(jieba.cut(place_type, cut_all=False))
    result = 0
    for j in range(len(place)):
        temp = np.array(pretrained_model.get_word_vector(place[j]))
        temp = temp.astype(np.float64)
        # print(type(q))
        if j == 0:
            result = temp
        else:
            result += temp
    result_place = list(result / len(place))
    # if i == 0:
    #     print(type(result_place[0]))
    all_temp['place'] = place_type
    all_temp['place_vector'] = result_place
    city_common = str(China_data['city'][i]) + str(China_data['area_name'][i]) + str(China_data['township'][i])
    city = list(jieba.cut(city_common, cut_all=False))
    result = 0
    for j in range(len(city)):
        temp = np.array(pretrained_model.get_word_vector(city[j]))
        temp = temp.astype(np.float64)
        # print(type(q))
        if j == 0:
            result = temp
        else:
            result += temp
            # print(type(q))

    result_city = result / len(city)
    all_temp['city'] = city_common
    all_temp['city_vector'] = list(result_city)
    patient_info = str(China_data['patient_info'][i])
    result_patient = 0
    if len(patient_info) > 3:
        patient = list(jieba.cut(patient_info, cut_all=False))
        result = 0
        for j in range(len(patient)):
            temp = np.array(pretrained_model.get_word_vector(patient[j]))
            temp = temp.astype(np.float64)
            if j == 0:
                result = temp
            else:
                result += temp
                # print(type(q))

        result_patient = result / len(patient)
    all_temp['patient_info'] = patient_info
    if len(patient_info) > 3:
        all_temp['patient_vector'] = list(result_patient)
    else:
        all_temp['patient_vector'] = 0
    time = str(China_data['time'][i])
    all_temp['time'] = time
    if i == 1:
        print(all_temp)
        print(type(all_temp['place_vector'][0]))
    all.append(all_temp)

data = json.dumps(all,ensure_ascii=False)
with open('data.json', 'w') as f:
    f.write(data)
