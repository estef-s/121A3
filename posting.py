class Posting:
    # The document name/id the token was found in.
    # Its tf-idf score for that document (for MS1, add only the term frequency
    docName = ""
    docID = -1
    score = -1

    def __init__(self, docID, score):
        self.docID = docID
        self.score = score
    
    def getDocID(self):
        return self.docID

    def getScore(self):
        return self.score

    
