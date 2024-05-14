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
    tokens_counter = 0
    #for d in docs:
    for dirpath, dirnames, filenames in os.walk('DEV'):
        for file in filenames:
            print(f'file{id}')
            id += 1
            filepath = os.path.join(dirpath, file)
            with open(filepath, 'r') as f:
                d = json.load(f)
                #parse & remove duplicates
                tokens = []
                tokens = tokenize(d)
                tokens_dict = computeWordFrequencies(tokens)

                for t in tokens_dict.keys():
                    # print(f'processed token{tokens_counter}')
                    #x = Posting(id, tokens_dict[t])
                    #if threshold < 1000:
                    #    with open(f"file{file_num}", 'a') as file:
                    #        file.write(f"{t}: {str(x)},")
                        #    threshold += 1
                    if t not in index_hash:
                        index_hash[t] = [Posting(id, tokens_dict[t])]

                        #index_hash[t] = f'{id},{tokens_dict[t]}'
                    # if t not in final_hash:
                    #     final_hash[t] = ''
                    
                    else:
                        index_hash[t].append(Posting(id, tokens_dict[t]))
                        #threshold = 0
                        #file_num += 1
                        #with open(f"file{file_num}", 'a') as file:
                        #    file.write(f"{t}: {str(x)},")
                        #    threshold += 1
                        # index_hash[t] = index_hash[t]+f' {id},{tokens_dict[t]}'


                    tokens_counter += 1
                    # if tokens_counter == 40000:
                    #     file_name = f"json_dumps/dump{file_num}"
                    #     with open(file_name, 'w') as out_file:
                    #         json.dump(index_hash, out_file)
                    #     tokens_counter = 0
                    #     file_num += 1
                    #     index_hash = {}
                            


                    # if t not in index_hash.keys():
                    #     posting_list = []
                    #     posting_list.append(Posting(id,tokens_dict[t]))
                    #     index_hash[t] = posting_list
                    # else:
                    #     index_hash[t].append(Posting(id,tokens_dict[t]))
    # line_num = 0
    # with open('master', 'w') as out:
    #     for key in final_hash.keys():
    #         final_hash[key] = (line_num)
    #         line_num += 1
    #         for dirpath, dirnames, filenames in os.walk('json_dumps'):
    #             for file in filenames:
    #                 filepath = os.path.join(dirpath, file)
    #                 with open(filepath, 'r') as f:
    #                     loaded_dict = json.load(f)
    #                     if key in loaded_dict.keys():
    #                         out.write(f'{loaded_dict[key]} ')
        
    # with open("memory_dict", "w") as memory:
    #     json.dump(final_hash, memory)

                    


    #file size
    with open('size_file', 'wb') as size_file:
        pickle.dump(index_hash, size_file)
    print(f"size: {sys.getsizeof(index_hash)}")
    print(f"number of documents {id}")
    print(f"number of words {len(index_hash.keys())}")
   
    return index_hash     


if __name__ == '__main__':
    buildIndex()
    
     
