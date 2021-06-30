import json
import aes_statistics

def compare_two_words(lemmaRefA,lemmaRefB):
	data = aes_statistics.load_data()
	contextA = collect_context(lemmaRefA, data)
	contextB = collect_context(lemmaRefB, data)
	sentence_comparison_dict = {}
	t = len(contextB) * len(contextA)
	print(f"Contexts for Lemma A: {len(contextA)}")
	print(f"Contexts for Lemma B: {len(contextB)}")
	for cA in contextA:
		for cB in contextB:
			common, total = compare_sentence_context(cA,cB)
			if (common, total) in sentence_comparison_dict.keys():
				sentence_comparison_dict[(common, total)] += 1
			else:
				sentence_comparison_dict[(common, total)] = 1
	for key in sentence_comparison_dict.keys():
		sentence_comparison_dict[key] = sentence_comparison_dict[key] / t

	print(sentence_comparison_dict)

def collect_context(lemmaRef,data):
	results = []
	for sentence in data:
		for token in sentence['token']:
			try:
				if lemmaRef == token['lemmaID']:
					results.append(sentence)
					break
			except KeyError:
				pass
	return results

def compare_sentence_context(contextA,contextB):
	# compare sentence features
	sentence_features_in_common = 0
	features_used = 0
	for feature in ('date','findspot'):
		try:
			features_used += 1
			if contextA[feature] == contextB[feature]:
				sentence_features_in_common += 1
		except KeyError:
			pass
	return sentence_features_in_common,features_used

def main(A,B):
	compare_two_words(A,B)

if __name__ == "__main__":
	main('78150','78030')

# 176860 TAz "word, phrase"
# 78030 mdw.t
# 78150 mdw