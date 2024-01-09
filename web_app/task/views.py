from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.urls import reverse
from .models import prod
# Create your views here.
#create forms instead of using html 

def index(request):
  if "task" not in request.session:
    request.session["task"]=[]
  players = prod.objects.all().values("name","price")
  return render(request,"task/index.html",{
    "task":request.session["task"],
    "players":players
  })
def add(request):
  if request.method== "POST":
    name = request.POST["name"]
    age = request.POST["age"]
    prod1 = prod(name=name,price=age)
    prod1.save()
    return HttpResponse("added")