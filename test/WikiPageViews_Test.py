__author__ = 'emill05'
import datetime
from WikiPageViews import WikiPageViews

def get_page_views_from_name_year_month():
    w = WikiPageViews()
    pageviews = w.get_page_views_from_name_year_month('John_Wick_(film)', '201410')
    viewsthirdoctober = pageviews['daily_views']['2014-10-03']
    assert viewsthirdoctober == 5121

def get_page_views_from_to_by_monthly():
    w = WikiPageViews()
    pageviews = w.get_page_views_from_to_by_monthly('John_Wick_(film)', datetime.date(2014,10,03), datetime.date(2014,10,05))
    assert pageviews[datetime.datetime(2014,10,03)] == 5121

get_page_views_from_to_by_monthly()