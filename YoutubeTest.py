__author__ = 'emill05'
from urllib2 import urlopen
import nltk
import json
from xml.dom import minidom
from YouTubeComments import YouTubeComments as yt
import gdata.youtube.service

# We will require read-only access to the YouTube Data and Analytics API.
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
  "https://www.googleapis.com/auth/yt-analytics.readonly"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_ANALYTICS_API_SERVICE_NAME = "youtubeAnalytics"
YOUTUBE_ANALYTICS_API_VERSION = "v1"

# Helpful message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = ""



def ListComments(jsonObject):
    commentString = ""
    for item in jsonObject["feed"]["entry"]:
        print item ["content"]["$t"]
        #print "======================================"
        commentString = commentString + item ["content"]["$t"]

    for item in jsonObject["feed"]["link"]:
        if (item["rel"] == "next"):
            GetNextPage(item["href"])


    #Analyze_comments(commentString)

def GetNextPage(url):
    comments = urlopen(url)
    ListComments(json.load(comments))


def GetComments(video_id):
    url = "https://gdata.youtube.com/feeds/api/videos/" + video_id + "/comments?alt=json&start-index=1&max-results=50&prettyprint=true&orderby=published"
    #url = "http://gdata.youtube.com/feeds/api/videos/" + video_id + "/comments?prettyprint=true"
    #url = "http://gdata.youtube.com/feeds/api/videos/" + video_id + "/comments?v=2&alt=json&start-index=1"
    comments = urlopen(url)
    ListComments(json.load(comments))


def Analyze_comments(comments):
    youtube = yt()
    print youtube.get_all_comments("FN3YaybNJ2s")


GetComments("2AUmvWm5ZDQ")
#for item in youtube.get_all_comments("FN3YaybNJ2s"):
#    test = test + item
#nltk.word_tokenize(test)

#ytfeed = yts.GetYouTubeVideoCommentFeed(video_id="pXhcPJK5cMc")

