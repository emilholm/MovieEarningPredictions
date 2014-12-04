#!/usr/bin/python

from oauth2client.tools import argparser
__author__ = 'emill05'
from datetime import datetime
import gdata.youtube.service
from googleapiclient.discovery import build


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
        search_response = self.youtube.search().list(q=title, part="id,snippet",
                                                     maxResults=results, order=order_by).execute()
        videos = {}

        for search_result in search_response.get("items", []):
            if "videoId" in search_result["id"]:
                videos[search_result["snippet"]["title"]] = search_result["id"]["videoId"]

        return videos

    def youtube_comments(self, video_id, until_date):
        comment_str = ''
        comment_feed = self.yts.GetYouTubeVideoCommentFeed(video_id=video_id)
        while comment_feed is not None:
            for comment in comment_feed.entry:
                date = datetime.strptime(comment.published.text[:10], "%Y-%m-%d")
                if (date <= until_date):
                    if comment.content.text is not None:
                        print comment.content.text
                        comment_str = comment_str + ' ' + comment.content.text
            next_link = comment_feed.GetNextLink()
            if next_link is None:
                comment_feed = None
            else:
                comment_feed = self.yts.GetYouTubeVideoCommentFeed(next_link.href)

        return comment_str

def main():
    y = YouTube('AIzaSyDQ6enre5eE7f_BIegK-2MOBbBAlMWaJgI')
    #blabla = y.youtube_search('Interstellar trailer', results=10)
    #print blabla
    comments = y.youtube_comments('uA59s-f8WqM', datetime(2014,10,10))
    print comments

if __name__ == '__main__':
    main()