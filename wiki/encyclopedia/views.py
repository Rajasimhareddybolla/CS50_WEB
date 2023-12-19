from django.shortcuts import render
from django.http import HttpResponse
from . import util
from django import forms
from random import randint
class search(forms.Form):
    entry = forms.CharField()

def index(request):
    if request.method=="POST":
        pass

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search":search(),
    })

def show(request,name="search"):
    name = name
    if request.method == "POST" and name=="search":
        form = search(request.POST)
        if form.is_valid():
            name=form.cleaned_data["entry"]
    if name.capitalize() in util.list_entries():
        about = util.get_entry(name)
        return render(request,"encyclopedia/encyclopedia.html",{
            "title":name,
            "context":about,
            "search":search(),
        })
    else:
        match_case = []
        
        for entry in util.list_entries():
            print(entry,name.capitalize())
            if entry.find(name.lower())!=-1:
                match_case.append(entry)
        return render(request,"encyclopedia/match.html",{
            "matchs":match_case
        })
def random(request):
    names = util.list_entries()
    entry = names[randint(0,len(names))]
    return show(request,entry)