# -*- coding: utf-8 -*-
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import nltk.tokenize
import re
#test

class Classifier():
    def __init__(self):
        self.train_classifier()


    def word_feats(self,words):
        return dict([(word, True) for word in words])


    def train_classifier(self):
        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')

        negfeats = [(self.word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
        posfeats = [(self.word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

        trainfeats = negfeats + posfeats

        self.classifier = NaiveBayesClassifier.train(trainfeats)


    def classify_text(self,text):
        porter = nltk.PorterStemmer() #use stemmer to normalize

        pattern = r"""(?ux)
        (?:[^\W\d_]\.)+
        | [^\W\d_]+(?:-[^\W\d_])*(?:’s)?
        | \d{4}
        | \d{1,3}(?:,\d{3})*
        | \$\d+(?:\.\d{2})?
        | \d{1,3}(?:\.\d+)?\s%
        | \.\.\.
        | [.,;"’?!():-_‘/]
        """

        words = re.findall(pattern, text)
        #stemmedWords = ''

        #wordlist = []

        #for word in words:
        #    try:
        #        #wordlist.append(porter.stem(word))
        #        stemmedWords = stemmedWords + ' ' + porter.stem(word)
        #        words.append(porter.stem(word))
        #    except:
        #        continue

        #print stemmedWords

        tokenizedWords = nltk.tokenize.sent_tokenize(text) #stemmedWords)

        negScore = self.classifier.prob_classify(self.word_feats(tokenizedWords)).prob('neg')
        posScore = self.classifier.prob_classify(self.word_feats(tokenizedWords)).prob('pos')
        return {'neg': negScore, 'pos': posScore}


def main():
    c = Classifier()
    score = c.classify_text('very bad terrible horrible boring')  #open('johnwickcomments.txt', 'r').read())
    print score['neg']
    print score['pos']

if __name__ == '__main__':
    main()
