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

class YouTube():
    def __init__(self):
        self.connect()


    def connect(self):
        client_secrets_file = "google_api.json"

        # We will require read-only access to the YouTube Data and Analytics API.
        youtube_scopes = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/yt-analytics.readonly"]
        youtube_api_service_name = "youtube"
        youtube_api_version = "v3"
        youtube_analytics_api_service_name = "youtubeAnalytics"
        youtube_analytics_api_version = "v1"

        # This variable defines a message to display if the CLIENT_SECRETS_FILE is
        # missing.
        missing_client_secrets_message = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

           %s

        with information from the Developers Console
        https://console.developers.google.com/

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           client_secrets_file))

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

        flow = flow_from_clientsecrets(client_secrets_file, message=missing_client_secrets_message, scope=" ".join(youtube_scopes))

        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run(flow, storage)

        http = credentials.authorize(httplib2.Http())
        self.yts = gdata.youtube.service.YouTubeService()
        self.youtube = build(youtube_api_service_name, youtube_api_version, http=http)


    def youtube_search(self, options):
        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = self.youtube.search().list(q=options.q,part="id,snippet",maxResults=options.max_results).execute()

        videos = {}

        for search_result in search_response.get("items", []):
            videos[search_result["snippet"]["title"]] = search_result["id"]["videoId"]

        return videos

    def youtube_comments(self, videoid):
        comment_feed = self.yts.GetYouTubeVideoCommentFeed(video_id=videoid)
        while comment_feed is not None:
            for comment in comment_feed.entry:
                yield comment
        next_link = comment_feed.GetNextLink()
        if next_link is None:
             comment_feed = None
        else:
             comment_feed = self.yts.GetYouTubeVideoCommentFeed(next_link.href)


def main():
    y = YouTube()
    VIDEO_ID = "TvCWWATPWbs"
    for comment in y.youtube_comments(VIDEO_ID):
        text = comment.content.text
        print text
    #argparser.add_argument("--q", help="Search term", default="The Dark Knight Rises Trailer")
    #argparser.add_argument("--max-results", help="Max results", default=50)
    #argparser.add_argument("--order", help="View Count", default="viewCount")
    #args = argparser.parse_args()
    #blabla = y.youtube_search(args)
    #print blabla

if __name__ == '__main__':
    main()