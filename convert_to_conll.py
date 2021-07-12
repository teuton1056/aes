from sklearn.base import MetaEstimatorMixin
import aes_statistics 
import json 
from conllu import TokenList
import html
import time
import csv
import tqdm

def load_conversion_tables():
	with open('upos_aes.json','r') as fp:
		upos_conversion_table = json.load(fp)
	return upos_conversion_table

def get_concordance():
	with open('concordance_name_text_id.csv','r',newline='',encoding='utf-8') as fp:
		reader = csv.reader(fp,delimiter='\t')
		return list(reader)

def lookup_tid(tid,source):
	for line in source:
		if line[1] == tid:
			return html.unescape(line[0])
	return 'n/a'

def convert_corpus(data):
	t = time.time()
	uct = load_conversion_tables()
	con = get_concordance()
	total = 0
	corpus = []
	for sentence in tqdm.tqdm(data):
		if check_sentence(sentence):
			total += 1
			s = convert_sentence(sentence,uct,con)
			corpus.append(s)
	print(corpus[0][0].keys())
	print(f"A total of {total} sentences have been converted")
	with open('corpus.conllu','w',encoding='utf-8') as fp:
		for sentence in corpus:
			fp.write(sentence.serialize())
	print("All Sentence Written")
	print(f"That took a total of {time.time() - t} seconds.")

def check_sentence(aes_sentence):
	for token in aes_sentence['token']:
		if 'hiero_unicode' not in token.keys():
			return False
	return True

def convert_sentence(aes_sentence,upos_conversion_table,con):
	def escape_underscore(original):
		new = ''
		for char in original:
			if char == '_':
				new += '-'
			else:
				new += char
		return new

	new_tokens = []
	# get sentence meta_data:
	metadata = {}
	metadata['sentid'] = aes_sentence['sentence_id']
	metadata['corpus'] = aes_sentence['corpus']
	metadata['src_text_id'] = aes_sentence['text']
	metadata['src_text'] = lookup_tid(aes_sentence['text'],con)
	metadata['owner'] = aes_sentence['owner']
	try:
		metadata['text_de'] = aes_sentence['sentence_translation']
	except Exception:
		print('No Translation')
	try:
		metadata['findspot'] = aes_sentence['findspot']
	except Exception:
		print('No Findspot')
	try:
		metadata['date'] = aes_sentence['date']
	except Exception:
		print('No Date')
	# get token data
	id_int_number = 1
	tokens = []
	for token in aes_sentence['token']:
		this_token = {
			'id':None,
			'form':None,
			'lemma':None,
			'upos':None,
			'xpos':None,
			'features':None,
			'head':None,
			'deprel':None,
			'deps':None,
			'misc':None,
		}
		this_token['id'] = id_int_number 
		id_int_number += 1
		# form and lemma
		this_token['form'] = html.unescape(token['hiero_unicode'])
		try:
			this_token['lemma'] = token['lemmaID']
		except:
			this_token['lemma'] = '_'
		try:
			this_token['misc'] = {
				'Translit':token['lemma_form']
			}
		except:
			pass
		# upos and xpos
		upos = '_'
		xpos = '_' # set default values
		if 'pos' in token.keys():
			xpos = escape_underscore(token['pos']) # try to change xpos
			try:
				upos = upos_conversion_table[xpos] # try to change upos
			except Exception:
				pass
			
		this_token['upos'] = upos
		this_token['xpos'] = xpos

		# try to do some features for nouns
		features = {} 
		number = {
			'singular':'Sing',
			'dual':'Dual',
			'plural':'Plur'
		}
		if 'numerus' in token.keys():
			try:
				features['Number'] = number[token['numerus']]
			except:
				pass
		if 'status' in token.keys():
			if token['status'] == 'st_constructus':
				features['Status'] = 'Cons'
			elif token['status'] == 'st_absolutus':
				features['Status'] = 'Abs'
			elif token['status'] == 'st_pronominalis':
				features['Status'] = 'Pron'
		gender = {
			'masculine':'Masc',
			'feminine':'Fem',
			'commonGender':'Com'
		}
		if 'genus' in token.keys():
			features['Gender'] = gender[token['genus']]
		
		# verb stuff
		voice = {'active':'Act','passive':'Pass'}
		if 'voice' in token.keys():
			features['Voice'] = voice[token['voice']]
		if 'morphology' in token.keys():
			if 'n-morpheme'	== token['morphology']:
				features['Aspect'] = 'Perf'
		if 'inflection' in token.keys():
			if token['inflection'] == 'infintive':
				features['VerbForm'] = 'Inf'
			elif token['inflection'] == 'pseudoParticiple':
				features['VerbForm'] = 'Conv'
			elif token['inflection'] == 'participle':
				features['VerbForm'] = 'Part'
			else:
				features['VerbForm'] = 'Fin'
			if token['inflection'] == 'suffixConjugation':
				features['Mood'] = 'Ind'
			if token['inflection'] == 'imperative':
				features['Mood'] = 'Imp'
	
		# other pos
		if 'pronoun' in token.keys():
			if token['pronoun'] == 'personal_pronoun':
				features['PronType'] = 'Prs'
			elif token['pronoun'] == 'demonstrative_pronoun':
				features['PronType'] = 'Dem'
			elif token['pronoun'] == 'interrogative_pronoun':
				features['PronType'] = 'Int'
			elif token['pronoun'] == 'relative_pronoun':
				features['PronType'] = 'Rel'
		
		this_token['features'] = features
		this_token['head'] = '_'
		this_token['deprel'] = '_'
		this_token['deps'] = '_'
		#this_token['misc'] = '_'
		new_tokens.append(this_token)
	new_sentence = TokenList(new_tokens)
	new_sentence.metadata = metadata
	return new_sentence


def main():
	data = aes_statistics.load_data_better()
	convert_corpus(data)

if __name__ == '__main__':
	main()