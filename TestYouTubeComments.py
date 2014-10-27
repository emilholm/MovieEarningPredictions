__author__ = 'martin'

from YouTubeComments import YouTubeComments as yt

youtube = yt()

print youtube.get_all_comments("b88XnNX8rnc")
print len(youtube.get_all_comments_from_last_call())
