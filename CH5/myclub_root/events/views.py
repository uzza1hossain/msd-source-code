from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import calendar
from calendar import HTMLCalendar


def index(request, year=date.today().year, month=date.today().month):
    # t = date.today()
    # month = date.strftime(t, '%b')
    # year = t.year
    year = int(year)
    month = int(month)
    if year < 2000 or year > 2099: year = date.today().year
    month_name = calendar.month_name[month]
    title = "MyClub Event Calendar - %s %s" % (month_name,year)
    cal = HTMLCalendar().formatmonth(year, month)
    # return HttpResponse("<h1>MyClub Event Calendar</h1>")
    # return HttpResponse("<h1>%s</h1>" % title)
    return HttpResponse("<h1>%s</h1><p>%s</p>" % (title, cal))
    
