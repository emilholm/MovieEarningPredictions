__author__ = "Martin Skytte"

from urllib2 import urlopen
import json
import sys


class YouTubeComments():
    """Class for handling YouTube comments
    """
    def __init__(self):
        """Set up the vars used in the YouTubeComments class
        :return:
        """
        self.url = ""
        self.next_url = ""
        self.comments = []

    def get_all_comments(self, video_id):
        """ Get All the comments from a YouTube video giving the video id.

        The id often looks similar to:
        FN3YaybNJ2s

        :param video_id:
        :return comments:
        """
        self.url = "https://gdata.youtube.com/feeds/api/videos/" + video_id + "/comments?alt=json&start-index=1&max-results=50&prettyprint=true&orderby=published"
        self.comments.extend(self.get_comment_from_page(self.url))

        while self.next_url != "":
            tmp = self.next_url
            self.next_url = ""
            self.comments.extend(self.get_comment_from_page(tmp))

        return self.comments

    def get_all_comments_from_last_call(self):
        return self.comments

    def get_comment_from_page(self, page_url):
        return_comments = []
        comments = urlopen(page_url)
        data = json.load(comments)

        try:
            if data["feed"]["entry"]:
                for item in data["feed"]["entry"]:
                    return_comments.append(item["content"]["$t"])
        except KeyError:
            sys.exc_info()[0]

        if data["feed"]["link"]:
            for item in data["feed"]["link"]:
                if item["rel"] == "next":
                    print item["href"]
                    self.next_url = item["href"]

        return return_comments
