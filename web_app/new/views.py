from django.http import HttpResponse
from django.shortcuts import render
import datetime
date = datetime.datetime.now()

# Create your views here
def index(request):
  return render(request,"new/index.html",{
    "year":date.month == 1 and date.day == 1
  })
