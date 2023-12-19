from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.
#create forms instead of using html 
class NewTaskForm(forms.Form):
  task=forms.CharField(label="task")
  age = forms.IntegerField(max_value=2,min_value=1)
def index(request):
  if "task" not in request.session:
    request.session["task"]=[]
  return render(request,"task/index.html",{
    "task":request.session["task"]
  })
def add(request):
  if request.method == "POST":
    form  = NewTaskForm(request.POST)
    if form.is_valid():
      task = form.cleaned_data["task"]
      request.session["task"] += [task]
    else:
      return render(request,"task/add.html",{
        "form":form
      })
  return render(request,"task/add.html",{
    "name":NewTaskForm()
  })
