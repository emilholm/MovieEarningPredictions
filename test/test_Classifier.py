__author__ = 'emill05'
from Classifier_old import Classifier

def classifier():
    c = Classifier()
    score = c.classify_text(open('johnwickcomments.txt', 'r').read())
    print score
    assert score['neg'] == 0.37
    assert score['pos'] == 0.63



classifier()