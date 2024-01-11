from django.shortcuts import render
from django.http import HttpResponse
from . import util
from django import forms
from random import randint
import markdown
from django.shortcuts import render
import markdown
from . import util
content = ""
class search(forms.Form):
    entry = forms.CharField()
class file(forms.Form):
    file_name = forms.CharField(max_length=255)
    text_area = forms.CharField(max_length=500,widget=forms.Textarea)

class EditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        try:
            contentt = []
            for line in args[0]:
                content.append(line)
        except:
            contentt="enter the md code hear"

        self.fields['content'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder':contentt}))

def index(request):
    if request.method=="POST":
        pass
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search":search(),
    })

def show(request, name="search"):
    name = name
    if request.method == "POST" and name == "search":
        form = search(request.POST)
        if form.is_valid():
            name = form.cleaned_data["entry"]
    if name.capitalize() in util.list_entries():
        about = util.get_entry(name)
        html = markdown.markdown(about)
        return render(request, "encyclopedia/preview.html", {
            'nam': name,
            'md': html,
        })
    else:
        match_case = []
        for entry in util.list_entries():
            entry = entry.lower()
            if entry.find(name.lower()) != -1:
                match_case.append(entry.capitalize())
        return render(request, "encyclopedia/match.html", {
            "matchs": match_case
        })
def random(request):
    names = util.list_entries()
    entry = names[randint(0,len(names)-1)]
    return show(request,entry)
def new(request):
    if request.method == "POST":
        form = file(request.POST)
        if form.is_valid():
            file_name = form.cleaned_data["file_name"]
            content = form.cleaned_data["text_area"]
        util.save_entry(file_name,content)
        return index(request)
    else:
        return render(request,"encyclopedia/add.html",{
            "feild":file,
        })
def edit(request,name="edit"):
    if request.method == "POST":
        conten = request.POST["edited"]
        util.save_entry(name,conten)
        return index(request)
    conten = util.get_entry(name)
    print(conten)
    return render(request,"encyclopedia/edit.html",{
        "name" :name.capitalize,
        "content":conten
    })
