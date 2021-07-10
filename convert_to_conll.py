from sklearn.base import MetaEstimatorMixin
import aes_statistics 
import json 
import conllu

with open('upos_aes.json','r') as fp:
	pos_conversion_table = json.load(fp)

pos_tags = set()
data = aes_statistics.load_data_better()

def convert_corpus(data):
	for sentence in data:
		convert_sentence(sentence)

def convert_sentence(aes_sentence,upos_conversion_table):
	# get sentence meta_data:
	metadata = {}
	metadata['sentid'] = aes_sentence['sentence_id']
	metadata['corpus'] = aes_sentence['corpus']
	metadata['src_text_id'] = aes_sentence['text']
	metadata['owner'] = aes_sentence['owner']
	try:
		metadata['text_de'] = aes_sentence['sentence_translation']
	except:
		print('No Translation')
	try:
		metadata['findspot'] = aes_sentence['findspot']
	except:
		print('No Findspot')
	try:
		metadata['date'] = aes_sentence['date']
	except:
		print('No Date')
	# get token data
	for token in aes_sentence['token']:
		# upos and xpos
		if 'pos' in token.keys():
			xpos = token['pos']
			try:
				upos = upos_conversion_table[xpos]
			except:
				upos = '_'
