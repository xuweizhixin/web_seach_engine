import math
words_score = {}
class BM25(object):
    """ Uses a SimpleIndex to score a document using Okapi BM 25.
    """
    def __init__(self, N, avg_l, k1=1.2, b=0.75):
        self.N = N
        #print N
        self.avg_l = avg_l
        #print avg_l
        self.k1 = k1
        self.b = b

    def idf_weight(self, term):
        """ Calculates the inverse document frequency weight of a term
        """
        # To make the formula clear, we set up local variables in terms of the 
        # mathematical description
        N = self.N
        num = words_map[term]
        ft = inverted_list[num-1].count(' ') - 1
        #print term
        #print ft
        #print math.log((N - ft + 0.5)/(ft + 0.5))
        return math.log((N - ft + 0.5)/(ft + 0.5))

    def score(self, document_id, query, common_term, l):
        """ Calculates the Okapi BM25 score for a document
        """
        # To make the formula clear, we set up local variables in terms of the 
        # mathematical description
        D = document_id
        k1 = self.k1
        b = self.b
        #docID_info = docID_url[document_id - 1].split()
        #l = int(docID_info[2])
        #l = common_len[document_id][0]
        avg_l = self.avg_l

        score = 0.0
        for term in query:
            idf = self.idf_weight(term)
            #num = words_map[term]
            #i = inverted_list[num - 1].split().index(str(document_id)) 
            #fdt = int(frequency[num - 1].split()[i])*1.0 / int(docID_info[3])
            fdt = common_term[term][document_id]
            
            #print "fdt"+str(fdt)
            s = idf * (fdt * (k1 + 1)) / (fdt + k1 * (1 - b + b*l/avg_l))
            #print "s:"+str(s)
            # Ignore negative scored terms (common terms)
            if s > 0.0:
                score += s

        return score

import pickle
import gzip
words_map = pickle.load(open('words.map', 'rb'))
inverted_list = gzip.open('inverted.list.gz', 'rb').readlines()
docID_url = gzip.open('docID_url.rpt.gz', 'rb').readlines()
frequency = gzip.open('frequency.rpt.gz', 'rb').readlines()

import string
def nextGEQ(old_words):
    words = ''
    for i in old_words.lower():
        if i in string.ascii_lowercase:
            words += i
        else:
            words += ' '
    contents = []
    query = []
    for word in words.split():
        if word in words_map:
            num = words_map[word]
            contents += [inverted_list[num-1].split()[1:]]
            query += [word]
        else:
            print "Your search - " + word + " - did not match any documents."
            continue
    if contents == []:
        print "Your search - " + old_words + " - did not match any documents."
        return

    common_list = []

    def mergeTwoList(a, b):
        clst = []
        i = 0
        j = 0
        while i < len(a) and j < len(b):
            ai = int(a[i])
            bj = int(b[j])
            if ai == bj:
                clst += [ai]
                i += 1
                j += 1
            elif ai < bj:
                i += 1
            elif ai > bj:
                j += 1
        return clst
               
    common_list = contents[0]
    for content in contents:
        common_list = mergeTwoList(common_list, content)
        #print common_list
        
    common_len = {}
    for document_id in common_list:
        docID_info = docID_url[document_id - 1].split()
        common_len[document_id] = [int(docID_info[2]), int(docID_info[3])]

    common_term = {}
    for term in query:
        num = words_map[term]
        term_list = inverted_list[num - 1].split()
        term_frequency = frequency[num - 1].split()
        common_doc = {}
        for document_id in common_list:
            #docID_info = docID_url[document_id - 1].split()
            #l = int(docID_info[2])
            i = term_list.index(str(document_id)) 
            common_doc[document_id] = int(term_frequency[i])*1.0 / common_len[document_id][1]
        common_term[term] = common_doc

    #for content in contents:
    #    common_list = common_list.intersection(set(content))

    #print common_list

    # Hard coded query

    # Load index
    N = len(docID_url)
    avg_l = 0.0
    for docID in docID_url:
        avg_l += int(docID.split()[2])
    avg_l = avg_l / N
    # Apply the BM25 model to our index
    bm25 = BM25(N, avg_l)

    # Score all documents
    scores = {}
    for i in common_list:
        scores[i] = bm25.score(i, query, common_term, common_len[i][0])
        #document = int(i)
        #scores[document] = bm25.score(document, query)

    sorted_docs = sorted(scores, key=lambda k: scores[k], reverse=True)

    print "Query for: " + ' '.join(query)
    for doc in sorted_docs[:10]:
        #print "%10.2f: %s"%(scores[doc], doc)
        print scores[doc], docID_url[doc - 1].split()[1]

#nextGEQ("happy new year")
while True: 
    s = raw_input('search\n')
    nextGEQ(s)
