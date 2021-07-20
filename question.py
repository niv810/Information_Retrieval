import math
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import creation
import json


def get_question(question):
    v = {}
    ps = PorterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    txt = tokenizer.tokenize(question)
    for term in txt:
        if term.lower() not in creation.stopwords:
            term = ps.stem(term.lower())
            if term not in v:
                v[term] = 0
            v[term] += 1
    return v


def get_question_vector(inverted_index, v):
    r = {}
    q_len = 0
    for term in v:
        if term in inverted_index:
            idf = inverted_index[term][0]
        else:
            continue
        tf = v[term]
        w = idf * tf
        docs = inverted_index[term][1]
        for doc in docs:
            if doc not in r:
                r[doc] = 0
            q_score = idf * docs[doc]
            r[doc] += w * q_score
            q_len += q_score
    q_len = math.sqrt(q_len)
    return r, q_len


def get_relevance_docs(r, q_len, docs_len):
    for doc in r:
        s = r[doc]
        doc_len = docs_len[doc]
        r[doc] = s / (doc_len * q_len)
    return dict(sorted(r.items(), key=lambda item: item[1], reverse=True))


def main():
    v = get_question(sys.argv[2])
    file = open(sys.argv[1])
    d = json.load(file)
    inverted_index = d["ir"]
    r, q_len = get_question_vector(inverted_index, v)
    docs_len = d["len_docs"]
    r = get_relevance_docs(r, q_len, docs_len)
    print(r)


if __name__ == "__main__":
    main()
