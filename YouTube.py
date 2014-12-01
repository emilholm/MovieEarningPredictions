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
    def __init__(self, developer_key):
        self.connect(developer_key)

    def connect(self, developer_key):
        # We will require read-only access to the YouTube Data and Analytics API.
        youtube_api_service_name = "youtube"
        youtube_api_version = "v3"

        self.yts = gdata.youtube.service.YouTubeService()
        self.youtube = build(youtube_api_service_name, youtube_api_version, developerKey=developer_key)

    def youtube_search(self, title, results=50, order_by='viewCount'):
        argparser.add_argument("--q", help="Search term", default=title)
        argparser.add_argument("--max-results", help="Max results", default=results)
        argparser.add_argument("--order", help="View Count", default=order_by)
        args = argparser.parse_args()

        search_response = self.youtube.search().list(q=args.q, part="id,snippet",
                                                     maxResults=args.max_results).execute()

        videos = {}

        for search_result in search_response.get("items", []):
            videos[search_result["snippet"]["title"]] = search_result["id"]["videoId"]

        return videos

    def youtube_comments(self, video_id, until_date):
        comment_feed = self.yts.GetYouTubeVideoCommentFeed(video_id=video_id)
        while comment_feed is not None:
            for comment in comment_feed.entry:
                date = datetime.strptime(comment.published.text[:10], "%Y-%m-%d")
                if (date <= until_date):
                    yield comment

        next_link = comment_feed.GetNextLink()
        if next_link is None:
            comment_feed = None
        else:
            comment_feed = self.yts.GetYouTubeVideoCommentFeed(next_link.href)


def main():
    y = YouTube()
    #video_id = "TvCWWATPWbs"
    #for comment in y.youtube_comments(video_id, datetime(2013,10,1)):
    #    text = comment.content.text
    #    text2 = comment.published.text
    #    print text + text2


    blabla = y.youtube_search('Dumb and dumber to trailer', results=10)
    print blabla

if __name__ == '__main__':
    main()