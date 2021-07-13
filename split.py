import conllu

def main():
	fp = open('corpus.conllu','r',encoding='utf-8')
	data = fp.read()
	fp.close()
	sentences = conllu.parse(data)
	corpora = {}
	for sentence in sentences:
		if sentence.metadata['corpus'] in corpora.keys():
			corpora[sentence.metadata['corpus']].append(sentence)
		else:
			corpora[sentence.metadata['corpus']] = [sentence]
	for corpus in corpora.keys():
		fp = open(f'./files/conllu_files/{corpus}.conllu','w',newline='',encoding='utf-8')
		for sentence in corpora[corpus]:
			fp.write(sentence.serialize())

def text_split():
	fp = open('corpus.conllu','r',encoding='utf-8')
	data = fp.read()
	fp.close()
	sentences = conllu.parse(data)
	texts = {}
	for sentence in sentences:
		if sentence.metadata['src_text_id'] in texts.keys():
			texts[sentence.metadata['src_text_id']].append(sentence)
		else:
			texts[sentence.metadata['src_text_id']] = [sentence]
	for text in texts.keys():
		fp = open(f'./files/conllu_files_by_text/{text}.conllu','w',newline='',encoding='utf-8')
		for sentence in texts[text]:
			fp.write(sentence.serialize())

if __name__ =="__main__":
	main()
	text_split()