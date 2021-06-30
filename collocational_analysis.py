import os 
import json
import numpy
from nltk import ngrams

def load_data():
	data = []
	files = os.listdir('./files/aes/')
	for file in files:
		if file.split('.')[-1] == 'json' and file[0] == '_':
			with open(f'./files/aes/{file}','r',encoding='utf-8') as fp:
				data.extend(list(json.load(fp).values()))
	return data

def ngram_generator(data,n):
	grams = []
	for sentence in data:
		tokens = sentence['token']
		a = ngrams(tokens,2)
		#grams = [tokens[i:i+n] for i in range(len(tokens)-n+1)]
		grams.extend(a)
	return grams

def counted_dictionary_words(data):
	counts = {}
	for sentence in data:
		#print(sentence)
		for item in sentence['token']:
			if 'lemmaID' in item.keys():
				if item['lemmaID'] in counts.keys():
					counts[item['lemmaID']] += 1
				else:
					counts[item['lemmaID']] = 1
	return counts

def counted_dictionary_bigrams(data):
	counts = {}
	for item in data:
		if 'lemmaID' in item[0].keys() and 'lemmaID' in item[1].keys():
			if (item[0]['lemmaID'],item[1]['lemmaID']) in counts.keys():
				counts[(item[0]['lemmaID'],item[1]['lemmaID'])] += 1
			else:
				counts[(item[0]['lemmaID'],item[1]['lemmaID'])] = 1
	return counts

def total_from_dict(dictionary):
	total = 0
	for entry in dictionary.keys():
		total += dictionary[entry]
	return total

def collocation_identification(AlemmaRef,BlemmaRef):
	raw_data = load_data()
	bigrams = ngram_generator(raw_data,2)
	lemmaCounts = counted_dictionary_words(raw_data)
	bigram_counts = counted_dictionary_bigrams(bigrams)
	Afreq = lemmaCounts[AlemmaRef]
	Bfreq = lemmaCounts[BlemmaRef]
	try:
		ABfreq = bigram_counts[(AlemmaRef,BlemmaRef)]
	except KeyError:
		print('That collocation never appears.')
		ABfreq = 0
	total_count = total_from_dict(lemmaCounts)
	MI = mutual_information(Afreq,Bfreq,ABfreq,total_count)
	TS = t_score(Afreq,Bfreq,ABfreq,total_count)
	print(MI,TS)


def mutual_information(A_freq,B_freq,AB_freq,total_count):
	numerator = AB_freq/total_count
	denominator = (B_freq/total_count)*(A_freq/total_count)
	return numpy.log2(numerator/denominator)

def t_score(A_freq,B_freq,AB_freq,total_count):
	# AB-((A*B) /TC)  /SQRT(AB)
	try:
		return (AB_freq - ((A_freq * B_freq)/total_count))/numpy.sqrt(AB_freq)
	except Exception as e:
		print('One of the values is impossible. ABref is probably 0',e)

# 5500344 nfr (adj)
# 854519 nfr (abstract)
# 78030 mdw.t
# 78150 mdw

collocation_identification('78030','854519')
#a = mutual_information(960,11847,44,12422985)
#print(a) #should be approx. 5.5868
#a = t_score(960,11847,44,12422985)
#print(a) # should be approx. 6.495
