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

def load_data_better():
	data = []
	files = os.listdir('./files/aes/')
	for file in files:
		if file.split('.')[-1] == 'json' and file[0] == '_':
			with open(f'./files/aes/{file}','r',encoding='utf-8') as fp:
				this_set = json.load(fp)
				for sid in this_set.keys():
					this_set[sid]['sentence_id'] = sid
					data.append(this_set[sid])
	return data

#with open('./files/aes/_aes_tb.json','r',encoding='utf-8') as fp:
#	data = list(json.load(fp).values())

def test():
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

if __name__ == '__main__':
	data = load_data_better()
	print(data[4])