from nltk.probability import FreqDist
from nltk.corpus import inaugural, stopwords
import string
import json
from pprint import pprint
import math
import networkx as nx

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

def get_buzzwords(docs):
	buzzwords = []
	for doc in docs:
		freqdist = FreqDist(docs[doc])
		vocab = freqdist.keys()
		freqs = freqdist.values()
		buzzwords = buzzwords + vocab[:50]

	buzzwords = set(buzzwords)

	freq_counts = {}
	for buzzword in buzzwords:
		print buzzword
		l = []
		for doc in docs:
			freqdist = FreqDist(docs[doc])
			t = (doc, freqdist[buzzword])
			l.append(t)
		freq_counts[buzzword] = l
	dump_content('freqs', freq_counts)
	return freq_counts

# docs = read_content('initial_processing')
docs = read_content('freqs')

# remove some random ascii chars that stuck around
del docs[u'\ufffd\ufffd']
del docs[u'\ufffd']

# get the top two speeches per buzzword
for doc in docs:
	docs[doc] = sorted(docs[doc],key=lambda x: x[1], reverse=True)[:2]
	docs[doc] = {docs[doc][0][0][:-4] : docs[doc][0][1], docs[doc][1][0][:-4] : docs[doc][1][1]}

dump_content("top_buzzwords", docs)

# Make dictionary for edge processing
for_edges = {}
for doc in docs:
	l = []
	for name in docs[doc]:
		l.append(name[0])
	for_edges[doc]=l

# make dictionary of edges between top two speeches for each buzzword
edge_dict = {}
for doc in for_edges:
	tuples = [(x,y) for x in for_edges[doc] for y in for_edges[doc] if x != y]
	for entry in tuples:
	    if (entry[1], entry[0]) in tuples:
	        tuples.remove((entry[1],entry[0]))
	edge_dict[doc] = tuples

# Make the graph
G=nx.Graph()
for doc in edge_dict:
	G.add_edges_from(edge_dict[doc])

# export graph to gexf so it can be read into Gephi
nx.write_gexf(G, 'speeches.gexf')



