import xml.etree.ElementTree as ET
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import sys
import math

total_docs = 0
ir = {}
len_docs = {}
d = {"ir": ir, "len_docs": len_docs}
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


# stop_words = nltk.corpus.stopwords.words('english')
def doc_part(v, doc, part):
    ps = PorterStemmer()
    txt = doc.findall(f"./{part}")
    tokenizer = RegexpTokenizer(r'\w+')
    txt = tokenizer.tokenize(txt[0].text)
    for term in txt:
        term = ps.stem(term.lower())
        if term not in stopwords:
            if term not in v:
                v[term] = 0
            v[term] += 1


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


def add_docs_from_files(path):
    global total_docs
    for i in range(74, 80):
        tree = ET.parse(f"{path}/cf{i}.xml")
        root = tree.getroot()
        for doc in root.findall(".//RECORD"):
            total_docs += 1
            v = corpus(doc)
            doc_id = doc.find("./RECORDNUM")
#            d["len_docs"][doc_id.text] = len(v)  # need to fix
            max_tf = max(v.values())
            for term in v:
                if term not in ir:
                    ir[term] = [0, {}]
                ir[term][0] += 1
                ir[term][1][doc_id.text] = v[term]/max_tf
#    total_docs = len(d["len_docs"])  # need to fix
    for term in ir:
        ir[term][0] = math.log2(total_docs/ir[term][0])
        idf = ir[term][0]
        for num_doc in ir[term][1]:
            tf = ir[term][1][num_doc]
            if num_doc not in len_docs:
                len_docs[num_doc] = 0
            len_docs[num_doc] += (idf * tf)**2
    for doc in len_docs:
        len_docs[doc] = math.sqrt(len_docs[doc])


def inverted_index(path):
    add_docs_from_files(path)
    j = json.dumps(d)
    f = open("vsm_inverted_index.json", "w")
    f.write(j)
    f.close()


def main():
    inverted_index(sys.argv[1])


if __name__ == "__main__":
    main()
