from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,items


def index(request):
    books = items.objects.all()
    print(books)
    return render(request, "auctions/index.html",{
        "books":books
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def add(request):
    if request.method == "POST":
        title = request.POST["Title"]
        discription = request.POST["Discription"]
        image = request.POST["Image"]
        ammount = request.POST["Bid"]
        item = items(Title = title,Discription=discription,Ammount=ammount,Image = image,user= request.user)
        item.save()
        return render(request, "auctions/index.html")
    return render(request,"auctions/add.html")
def view(request,name):
    print(items.objects.filter(Title=name),name)
    return render(request,"auctions/preview.html",{
        "book":items.objects.filter(Title=name)
     })