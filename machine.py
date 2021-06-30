#from pattern.vector import Document, NB
import conllu
import nltk
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

def get_data_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as fp:
        data = fp.read()
    sentences = conllu.parse(data)
    return sentences

def pos_tagged_words(data):
    tagged_words = []
    for sentence in data:
        for word in sentence:
            if word['upos'] != '_':
                tagged_words.append((word['form'],word['upos']))
    return tagged_words

def pos_tagged_words_ss(sentence):
    tagged_words = []
    for word in sentence:
        if word['upos'] != '_':
            tagged_words.append((word['form'],word['upos']))
    return tagged_words

def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word 
    in this case w1, w2, etc. must be of type str. Improvements to this function may have a significant effect on the behavior of the tagger"""
    if type(sentence[0]) is not str:
        raise TypeError(f"words must be of type str not type {type(sentence[0])}")
    return {
        'word': sentence[index],
        'is_first': index == 0,
        'is second': index == 1,
        'is_last': index == len(sentence) - 1,
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        'has_hyphen': '-' in sentence[index],
        'has_clitic': '=' in sentence[index],
        'has_.n': '.n' in sentence[index],
        'has_.': '.' in sentence[index],
        'word_length': len(sentence[index]),
        'position_in_sentence':index + 1
        }

def untag(tagged_sentence):
    return [w for w, t in tagged_sentence]

#
def main(token_list,EE=False,LE=False,ME=False,OE=False):
    # declare the fnames from which to pull data
    fnames = ['OE_Corpus','ME_Corpus','LE_Corpus','DE_Corpus']
    if EE:
        fnames = ['OE_Corpus','ME_Corpus']
    elif LE:
        fnames = ['LE_Corpus','DE_Corpus']
    elif ME:
        fnames = ['ME_Corpus']
    elif OE:
        fnames = ['OE_Corpus']
    else:
        pass
    data = []
    #pull syntax data from the files
    for fname in fnames:
        data.extend(get_data_from_file(f"corpora/{fname}.conllu"))

    #extract tagged sentences from the syntax data
    tagged_sentences = []
    for sentence in data:
        tagged_sentences.append(pos_tagged_words_ss(sentence))

    # Split the dataset for training and testing
    cutoff = int(.75 * len(tagged_sentences))
    training_sentences = tagged_sentences[:cutoff]
    test_sentences = tagged_sentences[cutoff:]

    print(f"Training on {len(training_sentences)} sentences")
    #print(f"Total Number of Test Sentences: {len(test_sentences)}")

    def transform_to_dataset(tagged_sentences):
        X, y = [], []
    
        for tagged in tagged_sentences:
            for index in range(len(tagged)):
                X.append(features(untag(tagged), index))
                y.append(tagged[index][1])
    
        return X, y
    
    X, y = transform_to_dataset(training_sentences)
    #print(X,y)

    clf = Pipeline([('vectorizer', DictVectorizer(sparse=False)),('classifier', DecisionTreeClassifier(criterion='entropy'))],verbose=True)
    
    #------------------
    #dvect = DictVectorizer(sparse=False)
    #aclf = DecisionTreeClassifier(criterion='entropy')
    #aX = dvect.fit_transform(X)
    #aclf.fit(aX,y)

    #------------------
    #time.sleep(10)
    clf.fit(X, y)
    
    #print('Training completed')
    
    X_test, y_test = transform_to_dataset(test_sentences)
    acc = clf.score(X_test, y_test)
    print(f"Accuracy on this run: {acc}")
    
    def pos_tag(sentence):
        tags = clf.predict([features(sentence, index) for index in range(len(sentence))])
        #tree.plot_tree(clf)
        return zip(sentence, tags)
 
    r = list(pos_tag(token_list))
    return r

#ir gm=k DAisw m At=f
if __name__ == "__main__":
    a = main(['ir','gm','=k','DAisw','m','At','=f'],EE=True)
    print(a)