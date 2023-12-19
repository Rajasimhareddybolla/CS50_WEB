from django.shortcuts import render
from .models import member
from django.template import loader
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request,"index.html",{
        "members":member.objects.all().values()
    })
def details(request,id):
    context = {
        "member":member.objects.all().values(),
    }
    template = loader.get_template("details.html")
    return render(request,"details.html",{
        "members" : member.objects.all()[id-1]
    })
def test(request):
    return render(request,"test.html",{
        "members":member.objects.all()
    })