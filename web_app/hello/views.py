from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
  return HttpResponse("hello  world ")

def wish(request):
  return HttpResponse("you are in wish function")
def greet(request,name):
  return render(request,"hello/greet.html",{"name":name})
