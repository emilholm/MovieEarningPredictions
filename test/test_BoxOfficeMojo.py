__author__ = 'emill05'
import datetime
from BoxOfficeMojo import BoxOfficeMojo

def get_search_results():
    b = BoxOfficeMojo()
    movie = b.get_search_results('John Wick')
    assert movie['John Wick'] == 'johnwick'

def get_movie_earnings():
    b = BoxOfficeMojo()
    earnings = b.get_movie_earnings('johnwick')
    assert len(earnings) > 38

def get_first_seven_days():
    b = BoxOfficeMojo()
    firstSevenDays = b.get_first_seven_days('johnwick')
    assert len(firstSevenDays) == 7

def get_release_date():
    b = BoxOfficeMojo()
    releaseDate = b.get_release_date('johnwick')
    dt = datetime.datetime(2014,10,24)
    assert releaseDate == dt

get_release_date()