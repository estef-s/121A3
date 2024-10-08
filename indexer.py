from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
#from krovetzstemmer import Stemmer
#from porter2 import stem
import json
import os
import pickle
import sys
import math
import time

from posting import Posting

docNames = {}
file_num = 1
total_docs = 0
docLengths = {}

def getText(doc):
    soup = BeautifulSoup(doc['content'], 'html.parser')
    text = soup.get_text()
    text = text.strip().lower()
    return text

def tokenize(doc):
    # soup = BeautifulSoup(doc['content'], 'html.parser')
    # text = soup.get_text()
    # text = text.strip().lower()
    text = getText(doc)

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
        #t = token.lower()
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

def buildIndex():
    global total_docs
    global docLengths
    index_hash = {}
    final_hash = {}
    id = 0
    global file_num # use for later
    threshold = 0
    docs_counter = 0
    #for d in docs:
    for dirpath, dirnames, filenames in os.walk('ANALYST'):
        for file in filenames:
            print(f'file{id}')
            id += 1
            filepath = os.path.join(dirpath, file)
            docs_counter += 1
            total_docs+=1

            with open(filepath, 'r') as f:
                #print(f)
                d = json.load(f)
                #parse & remove duplicates
                tokens = []
                tokens = tokenize(d)

                docLengths[id] = len(getText(d))

                tokens_dict = computeWordFrequencies(tokens)

                docNames[id] = d['url']

                for t in tokens_dict.keys():
                    # added tf weight to score
                    if t not in index_hash:
                        fscore = 1 + math.log10(tokens_dict[t])
                        index_hash[t] = [Posting(id, fscore)]
                    
                    else:
                        fscore = 1 + math.log10(tokens_dict[t])
                        index_hash[t].append(Posting(id, fscore))

            if docs_counter == 700:
                #essentially if we went through 10000 documents, dump into text file

                sorted_hash = dict(sorted(index_hash.items()))

                file_name = f"idx{file_num}.txt"
                with open(file_name, 'w') as out_file:
                    #counter = 1
                    for k,v in sorted_hash.items():
                        val_json_string = json.dumps([ob.__dict__ for ob in v]) #creating a json string for the list of posting objects
                        shi = {k: val_json_string} #dictionary of token to values_json_string
                        
                        dump_obj = json.dumps(shi)
                        out_file.write(dump_obj + '\n')

                out_file.close()        
                file_num += 1
                docs_counter = 0

    if docs_counter != 0: #if there are remaining ones at the end (if not multiples of 1000)
        #essentially if we went through 10000 documents, dump into text file

        sorted_hash = dict(sorted(index_hash.items()))

        file_name = f"idx{file_num}.txt"
        with open(file_name, 'w') as out_file:
            #counter = 1
            for k,v in sorted_hash.items():
                val_json_string = json.dumps([ob.__dict__ for ob in v]) #creating a json string for the list of posting objects
                shi = {k: val_json_string} #dictionary of token to values_json_string
                
                dump_obj = json.dumps(shi)
                out_file.write(dump_obj + '\n')

        out_file.close()        
        file_num += 1
        docs_counter = 0

    

    #dump docNames into file
    docs = open('docUrl.txt', 'w')
    json.dump(docNames, docs)
    #dump doclengths into file
    d_length = open('docLengths.txt','w')
    json.dump(docLengths, d_length)
    #merge files
    tempMerge = 'tempMerge.txt'
    mergeIndexes('idx1.txt', 'idx2.txt', tempMerge)
    mergeIndexes(tempMerge, 'idx3.txt', 'masterIndex.txt')
    #build index of index
    buildIndexofIndex()


    return index_hash     
    

#takes in files to merge and file to write to
def mergeIndexes(file1, file2, writeFile):
    
    combinedIndex = open(writeFile, 'w')
    idx1 = open(file1, 'r')
    idx2 = open(file2, 'r')
    line1 = idx1.readline()
    line2 = idx2.readline()

    while line1 and line2:

        l1Key = list(json.loads(line1).keys())[0]
        l2Key = list(json.loads(line2).keys())[0]
        if l1Key == l2Key:
            json_loads_line1 = list(json.loads(line1).values())[0]
            json_loads_line2 = list(json.loads(line2).values())[0]
            
            lv1 = json.loads(json_loads_line1)
            lv2 = json.loads(json_loads_line2)

            #FIX: check for duplicates
            master_list = lv1 + lv2
            val_json_string = json.dumps(master_list)
            shi = {l1Key: val_json_string} #dictionary of token to values_json_string
            dump_obj = json.dumps(shi)
            
            combinedIndex.write(dump_obj + '\n')
            line1 = idx1.readline()
            line2 = idx2.readline()
        elif l1Key < l2Key:
            combinedIndex.write(line1.strip() + '\n')
            line1 = idx1.readline()
        else:
            combinedIndex.write(line2.strip() + '\n')
            line2 = idx2.readline()
    

    if not line1:
        #print("index1 ended first")
        while line2:
            combinedIndex.write(line2.strip() + '\n')
            line2 = idx2.readline()
    else:
        #print("index2 ended first")
        while line1:
            combinedIndex.write(line1.strip() + '\n')
            line1 = idx1.readline()

    combinedIndex.close()
    idx1.close()
    idx2.close()
    


def buildIndexofIndex():
    global docLengths
    indexMap = {}
    addSize = 0
    position = 0
    with open('masterIndex.txt', 'r') as file1:
        with open("newMasterIndex.txt", 'w') as outfile:

            line = file1.readline()
            while line:
                json_line = json.loads(line)
                token = list(json_line.keys())[0]
                postings = json.loads(json_line[token])


                # print("THIS IS POSTINGS!!!!!!!", postings)

                #calculate IDF

               # print("TOTAL DOCS: ", total_docs)
               
             #   print("THIS IS TYPE|||||||||||||||||", type(postings))
                #docs_with_token = len(postings)

                visited = []
                for p_obj in list(postings):
                    if p_obj['docID'] not in visited:
                        visited.append(p_obj['docID'])
                    

                docs_with_token = len(visited)
                        
                


                # print("THIS IS DOCS_WITH_TOKEN ||||||||||||||||||||", docs_with_token)
                # #time.sleep(100)
                # if docs_with_token > total_docs:
                #     print("THIS IS DOCS|||||||||||||||||||||", docs_with_token)
                #     time.sleep(100)

               # print("DOCS W TOKENS: ", docs_with_token)
                idf_term = math.log10(total_docs/docs_with_token)

                


               # print("THIS IS DOCS W TOKEN!!!!!!!!!", docs_with_token)

                # print("THIS IS IDF_TERM!!!!!!!!!!!!!", idf_term)

                #time.sleep(10)

                #Calculate new score for every doc in term
                for post_obj in list(postings):
                   
                    post_obj['score'] = int(post_obj['score']) * idf_term
                        
                    #print("POST_OBJ", post_obj)    
                #break

                #push to new file
                postings = json.dumps(postings)
                new_line = json.dumps({token:postings}) +'\n'
                outfile.write(new_line)

                #jsonloads line
                indexMap[list(json_line.keys())[0]] = position
                addSize = len(new_line)
                position = position + addSize
                line = file1.readline()
        
    
    storeIndex = open('indexIndex.txt', 'w')
    #dump index into file
    json.dump(indexMap, storeIndex)
    storeIndex.close()

    #print(docLengths)
    return indexMap





if __name__ == '__main__':
    buildIndex()
