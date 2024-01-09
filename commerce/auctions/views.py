from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from . import admin
from .models import User,items,bids,catogeries
from django.shortcuts import redirect

def index(request):
    if request.method == "POST":
        name = request.POST["image"]
        if name:
            book = items.objects.get(Title=name)
            comment_set = bids.objects.filter(prodouct=book).values("comments")
            comments = []
            for comment in comment_set:
                comments.append(comment["comments"])
            statment = ""
            if request.user.is_authenticated:
                try:
                    bidded = bids.objects.get(prodouct = book,user = request.user).bid
                except:
                    bidded = bids(prodouct = book,user = request.user,bid = 0)
                    bidded.save()
                bidded = bids.objects.get(prodouct = book,user = request.user).bid
                try:
                    if bids.objects.get(prodouct = book,user = request.user).whishlist:
                        statment = "Remove from whish list"
                    else:
                        statment="add to whish list"
                except:
                    statment="add to whish list"
                prev_bids = bids.objects.filter(prodouct=book).values("bid","user") 

            else:
                prev_bids = "login to bid the item"
                bidded=0
            can_bid=True
            is_author = False
            if (bidded is None or bidded == 0):
                can_bid=True
                if book.user == request.user:
                    can_bid=False
                    is_author = True
            else:
                can_bid=False
            print(prev_bids )
            winner = None
            ammou = None   

            if book.Discription == "CLSOSED":
                max = bids.objects.filter(prodouct=book).order_by("bid").last()
                winner = max.user
                ammou = max.bid 
            return render(request,"auctions/preview.html",{
                "book":book,
                "bids_no":len(book.relations.all()),
                "comments":comments,
                "statment":statment,
                "can_bid":can_bid,
                "ammount":bidded,
                "is_author":is_author,
                "prev":prev_bids,
                "winneer":winner,
                "ammou":ammou,
                # "log":logged_in,
                "is_closed":book.Discription == "CLSOSED"
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
            print(username)
            user = User.objects.get(username = username)
            if user.is_superuser:
                admin.activate = True
                print(admin.activate)
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
        return redirect("index")
    else:
        return render(request, "auctions/register.html")

def add(request):
    if request.method == "POST":
        title = request.POST["Title"]
        discription = request.POST["Discription"]
        image = request.POST["Image"]
        ammount = request.POST["Bid"]
        desired_catogires = request.POST["categories"]
        item  = items(Title = title,Discription=discription,Ammount=ammount,Image = image,user= request.user)
  
        obj = catogeries(prodouct=item,catogery=desired_catogires)
        item.save()
        obj.save()
        return render(request, "auctions/index.html")
    return render(request,"auctions/add.html",{"catogeries":catogeries.catogeries.values()}
                  )
def bid(request):
    if request.method == "POST":
        bid_ammount = int(request.POST.get("bid_ammount"))
        user = request.user
        prodouct_image = request.POST["item"]
        prodouct = items.objects.get(Image=prodouct_image)
        if bid_ammount is None or prodouct is None:
            return HttpResponse("Invalid request")
        if not bid_ammount >= prodouct.Ammount:
            return HttpResponse("The bid amount must be greater than or equal to the fixed amount")
        bid = bids.objects.get(prodouct=prodouct, user=user)
        bid.bid = bid_ammount
        bid.save()
        return redirect("index")  # Redirect to the home page
def watch_list(request):
    if request.method == "POST":
        image = request.POST.get("image")
        prodouct = items.objects.get(Image = image)
        user = request.user
        try :
            bid = bids.objects.get(prodouct=prodouct,user=user)
            wish = bid.whishlist
        except:
            bid = bids(prodouct=prodouct,user=user)
            wish = False
   
        bid.whishlist=not(wish)
        bid.save()
        return redirect("index")
    prodoucts = []

    for prod in bids.objects.filter(user=request.user,whishlist=True).values("prodouct"):
        prodoucts.append(items.objects.get(pk=prod["prodouct"]))
    return render(request,"auctions/watch_list.html",{
        "books":prodoucts,
    }
    )
def permmisions():
    for user in User.objects.all:
        if not user.is_superuser:
            user.perm
def catogerie(request,cat):

    if cat !="raja":
        prodoucts = []
        print(catogeries.objects.filter(catogery=cat))
        for prod in catogeries.objects.filter(catogery=cat):
            prodoucts.append(prod.prodouct)
        print(prodoucts)
        return render(request,"auctions/catogeries.html",{
            "books":prodoucts,
            "cats":catogeries.catogeries.values(),
            "cat":cat
        })

    elif cat == "raja":
        return render(request,"auctions/catogeries.html",{

            "cats":catogeries.catogeries.values()
        })
def close(request):
    if request.method  == "POST":
        image = request.POST.get("url")
        prodouct=items.objects.get(Image=image)
        print(prodouct.Discription)
        prodouct.Discription="CLSOSED"
        prodouct.save()
    return redirect("index")