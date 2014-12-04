__author__ = 'emill05'
from YouTube import YouTube
from datetime import datetime

def func(x):
    return x + 1

def comments():
    y = YouTube('AIzaSyDQ6enre5eE7f_BIegK-2MOBbBAlMWaJgI')
    video_id = "wu0GCFD0ox4"
    untildate = datetime(2013,8,1)
    text = y.youtube_comments(video_id, untildate)
    assert len(text) > 100

    #uA59s-f8WqM



def test_answer():
    assert func(3) == 5


comments()

