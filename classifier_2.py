# -*- coding: utf-8 -*-
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
import nltk.tokenize
import re

class Classifier():
    def __init__(self):
        self.train_classifier()


    def _word_feats(self,words):
        return dict([(word, True) for word in words])

    def train_classifier(self):
        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')

        negfeats = [(self._word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
        posfeats = [(self._word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

        negcutoff = len(negfeats)*3/4
        poscutoff = len(posfeats)*3/4

        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

        self.classifier = NaiveBayesClassifier.train(trainfeats)
        self.classifier.show_most_informative_features(10)

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
        stemmedWords = []

        forbidden_words = set(stopwords.words('english'))

        for word in words:
            try:
                if word not in forbidden_words:
                    #stemmedWords = stemmedWords + ' ' + porter.stem(word)
                    stemmedWords.append(porter.stem(word))
                    #stemmedWords = stemmedWords + ' ' + word
            except:
                continue

        tokenizedWords = []

        for word in stemmedWords:
            try:
                tokenizedWords.append(nltk.tokenize.word_tokenize(word))
            except:
                continue

        #print tokenizedWords

        #tokenizedWords = nltk.tokenize.sent_tokenize(stemmedWords)
        #for word in words:


        negScore = self.classifier.prob_classify(self._word_feats(stemmedWords)).prob('neg') #classifier
        posScore = self.classifier.prob_classify(self._word_feats(stemmedWords)).prob('pos')
        return {'neg': negScore, 'pos': posScore}


def main():
    c = Classifier()
    score = c.classify_text(open('batman.txt', 'r').read())
    print score['neg']
    print score['pos']

if __name__ == '__main__':
    main()