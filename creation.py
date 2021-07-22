import xml.etree.ElementTree as ET
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import math

total_docs = 0
inverted_index = {}
len_docs = {}
d = {"inverted_index": inverted_index, "len_docs": len_docs}
stopwords = {"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out",
             "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into",
             "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the",
             "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were",
             "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to",
             "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have",
             "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can",
             "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself",
             "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by",
             "doing", "it", "how", "further", "was", "here", "than"}


# input: part of doc/ question, corpus
# this function tokenize the text, remove stopwords and punctuation marks, and add the stems to the corpus
def doc_tokenize(doc, v):
    ps = PorterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    txt = tokenizer.tokenize(doc)
    for term in txt:
        term = term.lower()
        if term.isalpha() and (term not in stopwords):
            term = ps.stem(term)
            if term not in v:
                v[term] = 0
            v[term] += 1


# building the corpus by the specific part (title/ extract/ abstract)
def doc_part(v, doc, part):
    txt = doc.findall(f"./{part}")
    doc_tokenize(txt[0].text, v)


# input: document
# output: corpus for the document
def corpus(doc):
    v = {}
    doc_part(v, doc, "TITLE")
    txt = doc.find("./EXTRACT")
    if txt is not None:
        doc_part(v, doc, "EXTRACT")
    txt = doc.find("./ABSTRACT")
    if txt is not None:
        doc_part(v, doc, "ABSTRACT")
    return v


# input: path to directory that contain the XML files
# the function building inverted index from every XML RECORD in the XML files and compute vector length for them
def add_docs_from_files(path):
    global total_docs
    for i in range(74, 80):
        tree = ET.parse(f"{path}/cf{i}.xml")
        root = tree.getroot()
        for doc in root.findall(".//RECORD"):
            total_docs += 1
            v = corpus(doc)
            doc_id = doc.find("./RECORDNUM")
            max_tf = max(v.values())
            for term in v:
                if term not in inverted_index:
                    inverted_index[term] = [0, {}]
                inverted_index[term][0] += 1
                inverted_index[term][1][int(doc_id.text)] = v[term] / max_tf
    for term in inverted_index:
        inverted_index[term][0] = math.log2(total_docs / inverted_index[term][0])
        idf = inverted_index[term][0]
        for num_doc in inverted_index[term][1]:
            tf = inverted_index[term][1][num_doc]
            if num_doc not in len_docs:
                len_docs[num_doc] = 0
            len_docs[num_doc] += (idf * tf)**2
    for doc in len_docs:
        len_docs[doc] = math.sqrt(len_docs[doc])


def create(path):
    add_docs_from_files(path)
    j = json.dumps(d)
    f = open("vsm_inverted_index.json", "w")
    f.write(j)
    f.close()
