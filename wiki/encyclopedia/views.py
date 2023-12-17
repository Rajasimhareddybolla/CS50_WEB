from django.shortcuts import render
from django.http import HttpResponse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def show(request,name):
    if name in util.list_entries():
        about = util.get_entry(name)
        return render(request,"encyclopedia/encyclopedia.html",{
            "title":name,
            "context":about
        })
    else:
        return HttpResponse(f"its not avaible {name}")
