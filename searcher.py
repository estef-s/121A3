import json
import indexer
from nltk.stem.porter import PorterStemmer
from indexer import docLengths


memoryIndex = {}
docNames = {}
def startEngine():
    #load index of index into memoryIndex
    global memoryIndex
    global docNames
    x = open('indexIndex.txt', 'r')
    y = open('docUrl.txt', 'r')
    memoryIndex = json.load(x)
    #print(memoryIndex.keys())
    #load doc names into docNames
    docNames = json.load(y)

   # print("THIS IS MEMORY INDEX\n", memoryIndex)

    while True:
        #take in input
        query = input("What do you want to search for?\n")
        
        #split up input
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in query.split()]
       
        #tokens = query.split()
        #print("THIS IS TOKENS\n", tokens)
        #print(tokens)
        
        tokenDict = {}
        for token in tokens:
            #get the posting lists from in masterindex.txt using seek
            y = findTokenList(token)
            x = json.loads(y)
            docIds = []
            for i in x:
                docIds.append(i.get('docID'))
            tokenDict[token] = set(docIds)

            
        #     print("THIS is X\n", docIds)
        #     print("THIS IS SET X\n", set(docIds))

        # print("TOKEN DICTIONARY", tokenDict)
        set_list = []
        for v in tokenDict.values():
            set_list.append(v)
       # print("THIS IS V\n", v)
        
        intersect_docID = list(set.intersection(*set_list))

        sorted_top_links = getdocURLS(cosineScore(tokens))
        #print("THIS IS INTERSECT DOCID", intersect_docID)
        #return intersection of list
        
        #go through docnames and match up doc ids w/ url
        #print("THIS IS docNAMES\n", docNames)
        urls = getdocURLS(intersect_docID)
        print(f"Here are the top 5 links for {query}:")

        test_top_links = []
        for i in range(len(urls)):
            if sorted_top_links[i] in urls:
                test_top_links.append(sorted_top_links[i])

        print(test_top_links[:5], "\n")
        #break


def findTokenList(token):
    #print("THIS IS TOKEN\n", token)
    with open('newMasterIndex.txt', 'r') as file:
        position = memoryIndex[token]
        file.seek(position)
        list_d = json.loads(file.readline()) #change to json.loads
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
    scores = {}
    length_ = [] 
    # stemmer = PorterStemmer()
    # tokens = [stemmer.stem(t) for t in query.split()]
    for t in query:
        posting_list = findTokenList(t)
        wordFreq = computeWordFrequencies(query)
       # print("THIS IS WORD FREQ", wordFreq)
        w_tq = wordFreq[t]
       # print("THIS iS POSTING LIST", posting_list)
       # print("THIS IS THE TYPE FOR POSTING LIST", type(posting_list))
        post_l = json.loads(posting_list)
        for pl in post_l:
            # print("this is PL", pl)
            # print(type(pl))
            # print(pl)
            scores[pl['docID']] += pl['score'] * w_tq
            

   
    #array_length = length_(scores.keys())
    for k in scores.keys():
        scores[k] = scores[k] / docLengths[k] # FIX LENGTH NUMBER (REPLACE 500)

    sorted_scores = sorted(scores, key = lambda x: scores[x], reverse = True)

    return sorted_scores
   

    
    # print("THIS IS sorted scores", sorted_scores)
    # print("THIS IS SCORES", scores)


    #print("THIS IS SCORES", scores)
    

    #return top k components         





if __name__ == '__main__':
    #indexer.buildIndex()
    startEngine()
