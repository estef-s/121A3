from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
#from krovetzstemmer import Stemmer
#from porter2 import stem
import json
import os
import pickle
import sys


from posting import Posting


def tokenize(doc):
    soup = BeautifulSoup(doc['content'], 'html.parser')
    text = soup.get_text()
    text = text.strip().lower()
    for tok in text:
        if tok == '':
            text.remove(tok)
            
    tokens = []
    token = ""

    #creating the Krovetz Stemmer object to stem tokens
    
    stemmer = PorterStemmer()
    for char in text:
        if char.isalnum() and char.isascii():
            token += char
        else:
            t = token.lower()
            if t != '':
                t = stemmer.stem(t)
                tokens.append(t)
                token = ""
    if token:
        token = stemmer.stem(token.lower())
        tokens.append(token)
    
    return tokens 

def computeWordFrequencies(tokenList):
    wordFreq = {}
    for token in tokenList:
        if token in wordFreq: # if already in dictionary, add to frequency otherwise set to 1
            wordFreq[token] += 1
        else: 
            wordFreq[token] = 1
    return wordFreq

# def porterStemmer(tokens):

#     stemmer = PorterStemmer()
#     stemmed_tokens = [stemmer.stem(t) for t in tokens]
#     return stemmed_tokens


def buildIndex():
    index_hash = {}
    final_hash = {}
    id = 0
    file_num = 1
    threshold = 0
    docs_counter = 0
    #for d in docs:
    for dirpath, dirnames, filenames in os.walk('ANALYST'):
        for file in filenames:
            print(f'file{id}')
            id += 1
            filepath = os.path.join(dirpath, file)
            docs_counter += 1

            with open(filepath, 'r') as f:
                d = json.load(f)
                #parse & remove duplicates
                tokens = []
                tokens = tokenize(d)
                tokens_dict = computeWordFrequencies(tokens)

                for t in tokens_dict.keys():
                    if t not in index_hash:
                        index_hash[t] = [Posting(id, tokens_dict[t])]
                    
                    else:
                        index_hash[t].append(Posting(id, tokens_dict[t]))

            if docs_counter == 10000:
                #essentially if we went through 10000 documents, dump into text file

                sorted_hash = dict(sorted(index_hash.items()))

                file_name = f"idx{file_num}"
                with open(file_name, 'w') as out_file:
                    for shi in sorted_hash.items:
                        dump_obj = json.dumps(shi)
                        out_file.write(dump_obj + '\n')
                out_file.close()        
                file_num += 1
                

    #file size
    # with open('size_file', 'wb') as size_file:
    #     pickle.dump(index_hash, size_file)
    # print(f"size: {sys.getsizeof(index_hash)}")
    # print(f"number of documents {id}")
    # print(f"number of words {len(index_hash.keys())}")
   
    return index_hash     
    

def mergeIndexes():
    #merge sort the files together
    print()


def buildIndexofIndexf():
    indexMap = {}
    addSize = 0
    position = 0
    with open('masterIndex.txt', 'r') as file:
        for line in file:
            #jsonloads line

            #line = file.readline()
            #indexMap[line[]] = position #add token to dict
            #addSize = len(line)
            print()
        
        indexIndex = open('indexMap')
        pickle.dump(index_hash, size_file)
    

if __name__ == '__main__':
    buildIndex()
    
     
