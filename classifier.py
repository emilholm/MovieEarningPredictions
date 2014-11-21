import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import nltk.tokenize
import re
 
def word_feats(words):
    return dict([(word, True) for word in words])
 
negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
 
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

print negfeats[0]

negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4
 
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
 
classifier = NaiveBayesClassifier.train(trainfeats)
print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
classifier.show_most_informative_features()

f = open('johnwickcomments.txt', 'r')
comments = '';
for item in f:
    comments = comments + item


words = comments.split() #use regex to clean text
stemmedwords = ['']

porter = nltk.PorterStemmer() #use stemmer to normalize

for word in words:
    try:
        print porter.stem(word)
    except StandardError:
        print('')

classifier.prob_classify(word_feats(['bullshit','bad','crap','shit','fuck'])).__dict__
#{'_prob_dict': {'neg': -0.5845758742331277, 'pos': -1.5857360646711278}, '_log': True} neg/pos=0,36

classifier.prob_classify(word_feats(['outstanding','amazing','good','great'])).__dict__
#{'_prob_dict': {'neg': -5.192535556923387, 'pos': -0.040001146956223366}, '_log': True} neg/pos=130

negScore = classifier.prob_classify(word_feats(words)).__dict__.values()[0]['neg']
#{'_prob_dict': {'neg': -67.37839930360587, 'pos': 0.0}, '_log': True}
posScore = classifier.prob_classify(word_feats(words)).__dict__.values()[0]['pos']

if negScore < posScore : print 'The text is POSITIVE'
else : print 'The text is NEGATIVE'

classifier.prob_classify(word_feats(words))

#classifier.classify(words)
#words.classify()