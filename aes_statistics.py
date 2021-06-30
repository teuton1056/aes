import json 
import os 

def load_data():
	data = []
	files = os.listdir('./files/aes/')
	for file in files:
		if file.split('.')[-1] == 'json' and file[0] == '_':
			with open(f'./files/aes/{file}','r',encoding='utf-8') as fp:
				data.extend(list(json.load(fp).values()))
	return data

#with open('./files/aes/_aes_tb.json','r',encoding='utf-8') as fp:
#	data = list(json.load(fp).values())

if __name__ == '__main__':
	print('Total Number of Sentences')
	dates = {}
	data = load_data()
	print(len(data))
	print(data[0])
	for sentence in data:
		date = sentence['date']
		if date not in dates.keys():
			dates[date] = 1
		else:
			dates[date] += 1
	print(dates)