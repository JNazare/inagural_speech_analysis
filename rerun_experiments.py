from nltk.probability import FreqDist
from nltk.corpus import inaugural, stopwords
import string
import json
from pprint import pprint
import math
import networkx as nx

# globals
filenames = inaugural.fileids()

def dump_content(filename, content):
	j = json.dumps(content, indent=4)
	f = open(filename+'.json', 'w')
	print >> f, j
	f.close()

def read_content(filename):
	json_data=open(filename+'.json')
	content = json.load(json_data)
	json_data.close()
	return content

def remove_punctuation(text):
	content = [w.strip(string.punctuation) for w in text]
	return content

def remove_stopwords(text):
	content = [w for w in text if w.lower() not in stopwords.words('english')]
	return content

def clean(text):
	content = [w.lower() for w in text if w != '']
	content = ' '.join(content)
	content = unicode(content, errors='replace')
	content = content.split()
	return content

def process_speech(filename):
	text = inaugural.words(filename)
	text = remove_punctuation(text)
	text = remove_stopwords(text)
	text = clean(text)
	return text

def process_speeches(filenames):
	texts = {}
	for filename in filenames:
		text = process_speech(filename)
		texts[filename] = text
	dump_content('initial_processing', texts)
	return texts

docs = read_content('initial_processing')
print len(docs.keys())

# Got buzzwords ==> put this in a function
# buzzwords = []
# for doc in docs:
# 	freqdist = FreqDist(docs[doc])
# 	vocab = freqdist.keys()
# 	freqs = freqdist.values()
# 	buzzwords = buzzwords + vocab[:50]

# buzzwords = set(buzzwords)
# # print buzzwords

# freq_counts = {}
# for buzzword in buzzwords:
# 	print buzzword
# 	l = []
# 	for doc in docs:
# 		freqdist = FreqDist(docs[doc])
# 		t = (doc, freqdist[buzzword])
# 		l.append(t)
# 	freq_counts[buzzword] = l
# print freq_counts
# dump_content('freqs', freq_counts)

docs = read_content('freqs')
del docs[u'\ufffd\ufffd']
del docs[u'\ufffd']

for doc in docs:
	docs[doc] = sorted(docs[doc],key=lambda x: x[1], reverse=True)[:2]

# Make list of edges
for_edges = {}
for doc in docs:
	l = []
	for name in docs[doc]:
		l.append(name[0])
	for_edges[doc]=l

edge_dict = {}
for doc in for_edges:
	tuples = [(x,y) for x in for_edges[doc] for y in for_edges[doc] if x != y]
	for entry in tuples:
	    if (entry[1], entry[0]) in tuples:
	        tuples.remove((entry[1],entry[0]))
	edge_dict[doc] = tuples

print len(docs.keys())

# Make the graph
G=nx.Graph()
for doc in edge_dict:
	G.add_edges_from(edge_dict[doc])

nx.write_gexf(G, 'speeches.gexf')



