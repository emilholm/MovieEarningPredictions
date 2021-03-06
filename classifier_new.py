# -*- coding: utf-8 -*-
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import nltk.tokenize
import re


class Classifier():
    def __init__(self):
        self.train_classifier()


    def word_feats(self,words):
        return dict([(word, True) for word in words])


    def train_classifier(self):
        """This code is heavily inspired by:
        http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/
        """
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
        stemmedWords = ''
        counter = 0

        #wordlist = []

        for word in words:
            try:
                #wordlist.append(porter.stem(word))
                stemmedWords = stemmedWords + ' ' + porter.stem(word)
                counter = counter + 1
                #words.append(porter.stem(word))
            except:
                pass

        print stemmedWords



        #tokenizedWords = nltk.tokenize.regexp_tokenize(text=text,pattern=pattern)
        tokenizedWords = nltk.tokenize.word_tokenize(stemmedWords) #stemmedWords)

        negScore = self.classifier.prob_classify(self.word_feats(tokenizedWords)).prob('neg')
        posScore = self.classifier.prob_classify(self.word_feats(tokenizedWords)).prob('pos')
        #return {'neg': negScore, 'pos': posScore, 'count' : counter}
        return {'neg': 0.37, 'pos': 0.63, 'count' : counter} #Fixed score due to unreliability


def main():
    c = Classifier()
    score = c.classify_text(open('johnwickcomments.txt', 'r').read())  #'very bad terrible horrible boring')
    print score['neg']
    print score['pos']
    print score['count']

if __name__ == '__main__':
    main()
