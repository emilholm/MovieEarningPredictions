__author__ = 'emill05'
from urllib2 import urlopen
import json
from xml.dom import minidom



def ListComments(jsonObject, count):
    for item in jsonObject["feed"]["entry"]:
        count += 1
        print "count: " + repr(count)
        print item ["content"]["$t"]
        print "======================================"

    for item in jsonObject["feed"]["link"]:
        if (item["rel"] == "next"):
            GetNextPage(item["href"], count)

def GetNextPage(url, count):
    comments = urlopen(url)
    ListComments(json.load(comments), count)


def GetComments(video_id):
    url = "https://gdata.youtube.com/feeds/api/videos/" + video_id + "/comments?alt=json&start-index=1&max-results=50&prettyprint=true&orderby=published"
    #url = "http://gdata.youtube.com/feeds/api/videos/" + video_id + "/comments?prettyprint=true"
    #url = "http://gdata.youtube.com/feeds/api/videos/" + video_id + "/comments?v=2&alt=json&start-index=1"
    count = 0
    comments = urlopen(url)
    ListComments(json.load(comments), count)


GetComments("FN3YaybNJ2s") #("n_y2rayU_y8")