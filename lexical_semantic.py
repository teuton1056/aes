import json
import aes_statistics
import matplotlib.pyplot as plt

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
	#compare_sentence_date(contextA,contextB)

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
	for feature in ('date','corpus'):
		try:
			features_used += 1
			if contextA[feature] == contextB[feature]:
				sentence_features_in_common += 1
		except KeyError:
			pass
	return sentence_features_in_common,features_used

def compare_sentence_date(contextA,contextB):
	sentence_datesA = {}
	sentence_datesB = {}
	for sA in contextA:
		# add this occurance of sA to the dict
		try:
			if sA['date'] in sentence_datesA.keys():
				sentence_datesA[sA['date']] += 1
			else:
				sentence_datesA[sA['date']] = 0
		except KeyError:
			pass
	for sB in contextB:
		# add this occurance of sA to the dict
		try:
			if sB['date'] in sentence_datesB.keys():
				sentence_datesB[sB['date']] += 1
			else:
				sentence_datesB[sB['date']] = 0
		except KeyError:
			pass

	# normalize values
	Btotal = sum(sentence_datesB.values())
	Atotal = sum(sentence_datesA.values())
	for key in sentence_datesB.keys():
		sentence_datesB[key] = sentence_datesB[key] / Btotal
	for key in sentence_datesA.keys():
		sentence_datesA[key] = sentence_datesA[key] / Atotal	
	print(sentence_datesA)
	print(sentence_datesB)

	# graph
	AOKFIP = sentence_datesA['OK & FIP']
	AMKSIP = sentence_datesA['MK & SIP']
	ANKSIP = sentence_datesA['NK']
	ATIPRO = sentence_datesA['TIP - Roman times']

	BOKFIP = sentence_datesB['OK & FIP']
	BMKSIP = sentence_datesB['MK & SIP']
	BNKSIP = sentence_datesB['NK']
	BTIPRO = sentence_datesB['TIP - Roman times']

	print([AOKFIP,AMKSIP,ANKSIP,ATIPRO])
	print([BOKFIP,BMKSIP,BNKSIP,BTIPRO])

	plt.plot([AOKFIP,AMKSIP,ANKSIP,ATIPRO],'r')
	plt.plot([BOKFIP,BMKSIP,BNKSIP,BTIPRO],'b')
	plt.show()

def main(A,B):
	compare_two_words(A,B)

if __name__ == "__main__":
	main('78150','78030')

# 176860 TAz "word, phrase"
# 78030 mdw.t
# 78150 mdw