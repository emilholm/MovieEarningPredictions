#!/usr/bin/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import httplib2
__author__ = 'emill05'
from datetime import datetime, timedelta
import httplib2
import os
import sys
import gdata.youtube.service

from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
from optparse import OptionParser

CLIENT_SECRETS_FILE = "google_api.json"

# We will require read-only access to the YouTube Data and Analytics API.
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
  "https://www.googleapis.com/auth/yt-analytics.readonly"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_ANALYTICS_API_SERVICE_NAME = "youtubeAnalytics"
YOUTUBE_ANALYTICS_API_VERSION = "v1"

# Helpful message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

now = datetime.now()
one_day_ago = (now - timedelta(days=1)).strftime("%Y-%m-%d")
one_week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")

parser = OptionParser()
parser.add_option("--metrics", dest="metrics", help="Report metrics",
  default="views,comments,favoritesAdded,favoritesRemoved,likes,dislikes,shares")
parser.add_option("--dimensions", dest="dimensions", help="Report dimensions",
  default="video")
parser.add_option("--start-date", dest="start_date",
  help="Start date, in YYYY-MM-DD format", default=one_week_ago)
parser.add_option("--end-date", dest="end_date",
  help="End date, in YYYY-MM-DD format", default=one_day_ago)
parser.add_option("--start-index", dest="start_index", help="Start index",
  default=1, type="int")
parser.add_option("--max-results", dest="max_results", help="Max results",
  default=10, type="int")
parser.add_option("--sort", dest="sort", help="Sort order", default="-views")
(options, args) = parser.parse_args()

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=" ".join(YOUTUBE_SCOPES))

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  credentials = run(flow, storage)

http = credentials.authorize(httplib2.Http())
yts = gdata.youtube.service.YouTubeService()

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=http)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = {}

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.

  for search_result in search_response.get("items", []):
      videos[search_result["snippet"]["title"]] = search_result["id"]["videoId"]

  #print "Videos:\n", "\n".join(videos), "\n"
  return videos

def youtube_comments(videoid):
    ytfeed = yts.GetYouTubeVideoCommentFeed(video_id=videoid)
    comments = [comment.content.text for comment in ytfeed.entry]
    return comments

argparser.add_argument("--q", help="Search term", default="The Dark Knight Rises Trailer")
argparser.add_argument("--max-results", help="Max results", default=50)
argparser.add_argument("--order", help="View Count", default="viewCount")
args = argparser.parse_args()
blabla = youtube_search(args)
print blabla.values()[0]
print youtube_comments(blabla.values()[0])
