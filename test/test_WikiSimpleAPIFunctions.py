__author__ = 'emill05'
from WikiSimpleAPIFunctions import WikiSimpleAPIFunctions
import datetime

def search_suggestions():
    w = WikiSimpleAPIFunctions()
    search_result = w.search_suggestions('John Wick')
    assert len(search_result) > 9

def page_created_date():
    w = WikiSimpleAPIFunctions()
    created_date = w.page_created_date('John_Wick_(film)')
    assert created_date == datetime.datetime(2013,12,20,17,57,15)


page_created_date()