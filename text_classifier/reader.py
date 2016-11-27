import re
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import linear_model
from sklearn import metrics

books = "books/"
books_after_stemming = "books stem/"
length_class = []
countVec_min_df = 1
svdOpt = 10
ngram_max = 2


def length_of_sentence_checker(ignore_3st):
    docs = []
    Y = []
    i = 1

    for subdir, dirs, files in os.walk(books):
        for f in files:
            if (ignore_3st and i % 3 != 0) or (not ignore_3st and i % 3 == 0):
                fp = open(books + f, encoding="utf8", errors='ignore')
                data = fp.read()

                data = data.replace("\n", " ")
                allData = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s|[.!?](?!\s)(?!\d)(?![g])", data)

                # usuniecie potencjalnych tytulow i nazwisk i niedokonczonego zdania na koncu
                del allData[0]
                del allData[0]
                del allData[-1]

                sum = 0
                for s in allData:
                    sum += len(s)
                docs.append(sum/len(allData))
                Y.append(f.split('_')[0])
            i += 1
    median = np.median(docs)
    min = np.min(docs)
    max = np.max(docs)
    length_class.append(min + (median -  min) / 2)
    length_class.append(median)
    length_class.append(median + (max - median) / 2)
    length_class.append(1000000)
    return docs, Y, length_class

def get_all_documents(ignore_3st):
    docs = []
    Y = []
    i = 1

    for subdir, dirs, files in os.walk(books_after_stemming):
        for f in files:
            if (ignore_3st and i % 3 != 0) or (not ignore_3st and i % 3 == 0):
                fp = open(books_after_stemming + f, encoding="utf8", errors='ignore')
                data = fp.read().replace('\n', ' ')
                docs.append(data)
                Y.append(f.split('_')[0])
            i += 1
    return docs, Y


def get_ngrams_and_countVect(text_data):
    count_vect = CountVectorizer(ngram_range=(1, ngram_max), lowercase=True, min_df=countVec_min_df)
    X = count_vect.fit_transform(text_data)
    return X, count_vect


def get_ngrams(text_data, cntvect):
    newVec = CountVectorizer(ngram_range=(1, ngram_max), lowercase=True, vocabulary=cntvect.vocabulary_)
    X = newVec.fit_transform(text_data)
    return X

def add_length_attribute(length_class, docs, docs_len):
    classes_names = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd']
    for i in range(0, len(docs)):
        j = 0
        while docs_len[i] > length_class[j]:
            j += 1
        # waga dlugosci zdan - wniosek: lepiej nie brac ich dlugosci pod uwage
        for t in range(0, 1):
            docs[i] += ' '+classes_names[j]
    return docs

if __name__ == '__main__':
    docs_len, Y_len, length_class = length_of_sentence_checker(True)
    docs, Y = get_all_documents(True)
    docs = add_length_attribute(length_class, docs, docs_len)

    test_docs_len, test_Y_len, l = length_of_sentence_checker(False)
    test_docs, test_Y = get_all_documents(False)
    test_docs = add_length_attribute(length_class, test_docs, test_docs_len)

    docs, cntvect = get_ngrams_and_countVect(docs)
    test_docs = get_ngrams(test_docs, cntvect)

    results = {'acc': [], 'prec': [], 'rec': [], 'f1': [], 'cm': []}

    clf = linear_model.LogisticRegression().fit(docs, Y)



    i = 0
    correct = 0
    for it_d in test_docs:
         predicted = clf.predict(it_d)
         if predicted[0] == test_Y[i]:
            correct += 1
            print(test_Y[i], predicted[0], ' +1')
         else:
             print(test_Y[i], predicted[0])
         # results['acc'].append(metrics.accuracy_score(test_Y[i], predicted[0]))
         # results['prec'].append(metrics.precision_score(test_Y[i], predicted[0], average='weighted'))
         # results['rec'].append(metrics.recall_score(test_Y[i], predicted[0], average='weighted'))
         # results['f1'].append(metrics.f1_score(test_Y[i], predicted[0], average='weighted'))
         # results['cm'].append(metrics.confusion_matrix(test_Y[i], predicted[0]))
         i += 1

    print (correct/i)
    # print ('Accuracy: %s, F1-measure: %s, Predicted: %s' % (np.mean(results['acc']), np.mean(results['f1']), np.mean(results['prec'])))
    # metricss = [np.mean(results['acc']), np.mean(results['f1']), np.mean(results['prec'])]