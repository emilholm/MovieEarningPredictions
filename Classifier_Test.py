__author__ = 'emill05'
from Classifier import Classifier

def classifier():
    c = Classifier()
    score = c.classify_text(open('johnwickcomments.txt', 'r').read())
    assert score['neg'] == 0.37
    assert score['pos'] == 0.63



classifier()