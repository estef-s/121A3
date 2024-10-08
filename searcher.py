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
    
    #query = input("What do you want to search for?\n")
    #split up input
    stemmer = PorterStemmer()
    time.time()
    tokens = [stemmer.stem(t) for t in query.split()]
    #tokens = query.split()
    #print("THIS IS TOKENS\n", tokens)
    #print(tokens)
    
    tokenDict = {}
    for token in tokens:
        #get the posting lists from in masterindex.txt using seek
        x = json.loads(findTokenList(token))
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
    #print("THIS IS INTERSECT DOCID", intersect_docID)
    #return intersection of list
    
    #go through docnames and match up doc ids w/ url
    #print("THIS IS docNAMES\n", docNames)
    urls = getdocURLS(intersect_docID)
    print(f"Here are the top 5 links for {query}:")
    print(urls[:5], "\n")
    #print(f"Search time: {(time.time()-start_time)*1000} ms\n")
    print(f"Search time: {(time.time()-start_time)*1000} ms\n")
    return urls


def findTokenList(token):
    #print("THIS IS TOKEN\n", token)
    with open('newMasterIndex.txt', 'r') as file:
        position = memoryIndex[token]
        file.seek(position)
        list_d = json.loads(file.readline()) #change to json.loads
        print(type(list_d))
    #print("THIS IS LIST\n", list[token])
    return list_d[token]

def getdocURLS(docList):
    urlList = []
    #print("TESTING\n", docNames[772])
    for doc in docList:
        urlList.append(docNames[str(doc)])
    return urlList

if __name__ == '__main__':
    #indexer.buildIndex()
    startEngine()
