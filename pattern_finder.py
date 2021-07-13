import conllu
import csv
import numpy as np
import tqdm

def conditional_prob_A_given_B(count_AB,count_B):
	return count_AB / count_B

def probabilityA(count_A,total):
	return count_A / total 

def independacy_test(count_A,count_B,count_AB,total):
	c = conditional_prob_A_given_B(count_AB,count_B)
	a = probabilityA(count_A,total)
	if c == a:
		return 0, 0.0
	else:
		diff = abs(c - a)
		mean = (c+a) / 2 
		perc_diff = (diff / mean) * 100
		return diff, perc_diff

def mutual_information(count_A,count_B,count_AB,total):
	if count_A != 0 or count_B != 0:
		return np.log2((count_AB/total)/((count_A/total)*(count_B/total)))
	else:
		return 0

def tscore(count_A,count_B,count_AB,total):
	if count_AB != 0:
		a = count_AB - (count_A*count_B)/total
		return a / np.sqrt(count_AB)
	else:
		return 0

def write_results(name,count_A,count_B,count_AB,total):
	if count_AB > 0:
		row = [str(i) for i in [name,count_A,count_B,count_AB,total]]
		diff, perc_diff = independacy_test(count_A,count_B,count_AB,total)
		row.append(str(diff))
		row.append(str(perc_diff))
		mi = mutual_information(count_A,count_B,count_AB,total)
		ts = tscore(count_A,count_B,count_AB,total)
		row.extend([str(mi),str(ts)])
		fp = open('pattern_finder_results.csv','a',newline='',encoding='utf-8')
		fp.write('\t'.join(row))
		fp.write('\n')

def get_counts_Bsent(entryA,valueA,meta_entry,meta_value,conll_data):
	b_counts = 0
	a_counts = 0
	ab_counts = 0
	total = 0
	for sentence in conll_data:
		b = False
		if sentence.metadata[meta_entry] == meta_value:
			b_counts += 1
			b = True
		for token in sentence:
			total += 1
			if token[entryA] == valueA:
				a_counts += 1
				if b:
					ab_counts += 1

	return a_counts,b_counts,ab_counts,total

def load_conll_data():
	fp = open('./corpus.conllu',encoding='utf-8')
	data = fp.read() 
	fp.close() 
	sentences = conllu.parse(data)
	return sentences

def get_every_word_data(sent_data,e):
	words = set()
	for sentence in sent_data:
		for token in sentence:
			if token[e] != '_':
				words.add(token[e])
	return list(words)

def get_every_meta(sent_data,e): # gets a list of every possible entry in a metadata spot
	entries = set()
	for sentence in sent_data:
		entries.add(sentence.metadata[e])
	return entries

def main():
	sent_data = load_conll_data()
	Ae = 'lemma'
	Be = 'corpus'
	A = get_every_word_data(sent_data,Ae)
	B = get_every_meta(sent_data,Be)
	for a in tqdm.tqdm(A):
		for b in B:
			ac,bc,abc,tc = get_counts_Bsent(Ae,a,Be,b,sent_data)
			write_results(f"{Ae}{a}:{Be}{b}",ac,bc,abc,tc)

main()