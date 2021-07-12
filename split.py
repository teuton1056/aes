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

if __name__ =="__main__":
	main()