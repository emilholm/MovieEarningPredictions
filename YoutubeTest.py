__author__ = 'emill05'
from urllib2 import urlopen
import json
from xml.dom import minidom



def ListComments(jsonObject):
    for item in jsonObject["feed"]["entry"]:
        print item ["content"]["$t"]
        print "=======234==============================="

    for item in jsonObject["feed"]["link"]:
        if (item["rel"] == "next"):
            GetNextPage(item["href"])

def GetNextPage(url):
    comments = urlopen(url)
    ListComments(json.load(comments))


def GetComments(video_id):
    url = "https://gdata.youtube.com/feeds/api/videos/" + video_id + "/comments?alt=json&start-index=1&max-results=50&prettyprint=true&orderby=published"
    #url = "http://gdata.youtube.com/feeds/api/videos/" + video_id + "/comments?prettyprint=true"
    #url = "http://gdata.youtube.com/feeds/api/videos/" + video_id + "/comments?v=2&alt=json&start-index=1"
    comments = urlopen(url)
    ListComments(json.load(comments))


GetComments("FN3YaybNJ2s") #("n_y2rayU_y8")