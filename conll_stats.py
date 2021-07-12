import conllu 
import os 
import json
import numpy

fnames = os.listdir('./files/conllu_files/')
statistics = {}
for fname in fnames: # this will iterate over each corpus file
	corpus_stats = {}
	fp = open(f'./files/conllu_files/{fname}','r',encoding='utf-8')
	data = fp.read()
	fp.close()
	corpus_sentences = conllu.parse(data)
	corpus_stats['Total Number of Sentences'] = len(corpus_sentences)
	total_words = 0
	sentence_lengths = []
	dates = {}
	corpus_name = corpus_sentences[0].metadata['corpus']
	for sentence in corpus_sentences:
		sentence_lengths.append(len(sentence))
		if sentence.metadata['date'] in dates.keys():
			dates[sentence.metadata['date']] += 1
		else:
			dates[sentence.metadata['date']] = 1
		for token in sentence:
			total_words += 1
	corpus_stats['Total Words'] = total_words
	corpus_stats['Dates'] = dates
	corpus_stats['Average Sentence Length'] = numpy.mean(sentence_lengths)
	statistics[corpus_name] = corpus_stats

with open('corpus_stats.json','w') as fp:
	fp.write(json.dumps(statistics))