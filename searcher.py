import json

memoryIndex = {}
docNames = {}
def startEngine():
    #load index of index into memoryIndex
    memoryIndex = json.load('indexIndex.txt')
    #load doc names into docNames
    docNames = json.load('docUrl.txt')

    while True:
        #take in input
        query = input()
        #split up input
        tokens = query.split()
        
        tokenDict = {}
        for token in tokens:
            #get the posting lists from in masterindex.txt using seek
            tokenDict[token] = findTokenList(token)
        
        #return intersection of lists
        commonDocs = []
        #go through docnames and match up doc ids w/ url
        urls = getdocURLS(commonDocs)
        print(urls)
        break


def findTokenList(token):
    with open('masterIndex.txt', 'r') as file:
        position = memoryIndex[token]
        file.seek(position)
        list = file.readline() #change to json.loads
    return list

def getdocURLS(docList):
    urlList = []
    for doc in docList:
        urlList.append(docNames[doc])
    return docList

if __name__ == '__main__':
    startEngine()