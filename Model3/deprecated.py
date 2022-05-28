'''
code used before
'''
# count input_size
# input_size = 0
# for city in data.values():
# 	if input_size != 0:
# 		break
# 	for p in city:
# 		if type(p['patient_vector']) == list:
# 			input_size = len(p['patient_vector'])
# 			break

# def clean_useless(f1,f2):
# 	with open(f1) as f:
# 		data = json.load(f)
# 	for i in data.values():
# 		for j in i:
# 			del j["place_vector"]
# 			del j["city_vector"]
# 	json.dump(data,open(f2,'w'),ensure_ascii=False)
# for i in range(3):
# 	if not exists('data_'+str(i)+'.json'):
# 		clean_useless('classified_data_'+str(i)+'.json','data_'+str(i)+'.json')

# datas = {}
# for city_string in train_city:
# 	city = data[city_string]
# 	start_date = datetime.strptime(city[0]['time'],'%Y:%m:%d')
# 	end_date = datetime.strptime(city[-1]['time'],'%Y:%m:%d')
# 	CNT = []
# 	VECTOR = []
# 	while start_date < end_date:
# 		cnt = 0
# 		vector = []
# 		for p in city:
# 			if p['time'] == (start_date).strftime('%Y:%m:%d'):
# 				cnt += 1
# 				vector.append(p['patient_vector'])
# 		if any((type(v)==np.ndarray for v in vector)):
# 			vector = np.array([v for v in vector if type(v)==np.ndarray])
# 			vector = np.mean(vector,axis=0)
# 		else:
# 			vector = np.zeros((input_size,))
# 		CNT.append(cnt)
# 		VECTOR.append(vector)
# 		start_date += timedelta(days=1)
# 	CNT = np.array(CNT)
# 	VECTOR = np.array(VECTOR)
# 	temp = np.hstack((CNT.reshape(-1,1),VECTOR))
# 	datas[city_string] = temp

# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")