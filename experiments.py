from nltk.corpus import inaugural, stopwords
# from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora, models, similarities
import re
import string

filenames = inaugural.fileids()
# lmtzr = WordNetLemmatizer()
filtered_speeches = []

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

for filename in filenames:
	print filename
	print "Reading in raw words..."
	raw_words = inaugural.words(filename)
	print "Removing stop words..."
	filtered_words = [word for word in raw_words if not word in stopwords.words('english')]
	print "Removing punctuation..."
	filtered_words = [word.strip(string.punctuation) for word in filtered_words]
	filtered_words = [word.lower() for word in filtered_words if word != ""]
	tokens_once = set(word for word in set(filtered_words) if filtered_words.count(word) == 1)
	filtered_words = [removeNonAscii(word) for word in filtered_words if word not in tokens_once]
	print "Appending filtered words..."
	filtered_speeches.append(filtered_words)

print "making numbered corpus..."
dictionary = corpora.Dictionary(filtered_speeches)
corpus = [dictionary.doc2bow(text) for text in filtered_speeches]
tfidf = models.TfidfModel(corpus)
print tfidf
