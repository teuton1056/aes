import aes_statistics

def find_spellings(lemma_id,mode='hiero_unicode'): # acceptable modes are 'hiero_unicode' 'hiero_inventar' and 'hiero'
	data = aes_statistics.load_data()
	total_spellings = 0
	results = {}
	for sentence in data:
		for token in sentence['token']:
			if 'lemmaID' in token.keys():
				if lemma_id == token['lemmaID']:
					if mode in token.keys():
						total_spellings += 1
						if token[mode] in results.keys():
							results[token[mode]] += 1
						else:
							results[token[mode]] = 1
	return total_spellings, results 

def main():
	total, results = find_spellings('78030',mode='hiero')
	print(f'A Total of {total} spellings were analyzed with the following results:')
	print(results)

if __name__ == '__main__':
	main()