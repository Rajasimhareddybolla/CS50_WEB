from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,items,bids


def index(request):

    if request.method == "POST":
        name = request.POST["image"]
        if name:
            return render(request,"auctions/preview.html",{
                "book":items.objects.get(Title=name)
            })
        return reverse(request,index)
    books = items.objects.all()
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
    """
    Logs out the user and redirects to the index page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the index page.
    """
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
