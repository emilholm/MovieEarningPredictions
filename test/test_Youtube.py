__author__ = 'emill05'
from YouTube import YouTube
from datetime import datetime


def comments():
    y = YouTube('AIzaSyDQ6enre5eE7f_BIegK-2MOBbBAlMWaJgI')
    video_id = "wu0GCFD0ox4"
    untildate = datetime(2013,8,1)
    text = y.youtube_comments(video_id, untildate)
    assert len(text) > 100

def youtube_search():
    y = YouTube('AIzaSyDQ6enre5eE7f_BIegK-2MOBbBAlMWaJgI')
    result = y.youtube_search('John Wick trailer')
    assert len(result) > 40

    #uA59s-f8WqM



youtube_search()

