import json
import indexer
from nltk.stem.porter import PorterStemmer
import time 



memoryIndex = {}
docNames = {}

def setUP():
    global memoryIndex
    global docNames
    #load index of index into memoryIndex
    x = open('indexIndex.txt', 'r')
    y = open('docUrl.txt', 'r')
    memoryIndex = json.load(x)
    #print(memoryIndex.keys())
    #load doc names into docNames
    docNames = json.load(y)

def startEngine(query):
    #take in input
    
    start_time = time.time()
    stemmer = PorterStemmer()
    time.time()
    tokens = [stemmer.stem(t) for t in query.split()]
   
    tokenDict = {}
    for token in tokens:
        #get the posting lists from in masterindex.txt using seek
        x = json.loads(findTokenList(token))
        docIds = []
        for i in x:
            docIds.append(i.get('docID'))
        tokenDict[token] = set(docIds)

        
   
    set_list = []
    for v in tokenDict.values():
        set_list.append(v)
    # print("THIS IS V\n", v)
    
    intersect_docID = list(set.intersection(*set_list))
    sorted_top_links = getdocURLS(cosineScore(tokens))
    x = cosineScore(tokens)
    #print("THIS IS X: |||||||||||||||||||", x)
   
    urls = getdocURLS(intersect_docID)
    #print(f"Here are the top 5 links for {query}:")
    test_top_links = []
    for i in range(len(urls)):
        if sorted_top_links[i] in urls:
            test_top_links.append(sorted_top_links[i])

    print(test_top_links[:5], "\n")
    print(f"Search time: {(time.time()-start_time)*1000} ms\n")
    return test_top_links[:10]


def findTokenList(token):
    #print("THIS IS TOKEN\n", token)
    
    with open('newMasterIndex.txt', 'r') as file:
        position = memoryIndex[token]
        file.seek(position)
        list_d = json.loads(file.readline()) #change to json.loads
        #print(type(list_d))
    #print("THIS IS LIST\n", list[token])
    return list_d[token]

def getdocURLS(docList):
    urlList = []
    #print("TESTING\n", docNames[772])
    for doc in docList:
        urlList.append(docNames[str(doc)])
    return urlList



def computeWordFrequencies(tokenList):
    wordFreq = {}
    for token in tokenList:
        if token in wordFreq: # if already in dictionary, add to frequency otherwise set to 1
            wordFreq[token] += 1
        else: 
            wordFreq[token] = 1
    return wordFreq

def cosineScore(query):
    global doc_lengths
    scores = {}
    length_ = [] 
    
    for t in query:
        posting_list = findTokenList(t)
        wordFreq = computeWordFrequencies(query)
        w_tq = wordFreq[t]
       
        post_l = json.loads(posting_list)
        for pl in post_l:
           
            if pl['docID'] not in scores:
                scores[pl['docID']] = pl['score'] * w_tq
            else: 
                scores[pl['docID']] += pl['score'] * w_tq

    
    #array_length = length_(scores.keys())
    z = open('docLengths.txt', 'r')
    doc_lengths = json.load(z)
    #print(doc_lengths)
    for k in scores.keys():
        scores[k] = scores[k] / doc_lengths[str(k)] # FIX LENGTH NUMBER (REPLACE 500)

    sorted_scores = sorted(scores, key = lambda x: scores[x], reverse = True)


    return sorted_scores

if __name__ == '__main__':
    #indexer.buildIndex()
    setUP()
    startEngine('master of software engineering')


