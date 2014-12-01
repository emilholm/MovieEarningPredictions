__author__ = 'emill05'
from YouTube import YouTube

def func(x):
    return x + 1

def comments():
    y = YouTube()
    video_id = "TvCWWATPWbs"

    for comment in y.youtube_comments(video_id):
        text = comment.content.text
        print text

    assert len(text) > 100



def test_answer():
    assert func(3) == 5


comments()

