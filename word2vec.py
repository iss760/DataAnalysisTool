import gensim

class Word2Vec:
    def __init__(self):
        self.MODEL_PATH = "./ko/"
        self.MODEL_NAME = 'ko.bin'
        self.model = gensim.models.Word2Vec.load(self.MODEL_PATH + self.MODEL_NAME)

    def similarity(self, word):
        return self.model.wv.most_similar(word)
