import json
from time import sleep
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User,post,link
from  django.core.paginator import Paginator


def index(request,name=''):

    posts_list =post.objects.all().order_by('time').reverse()
    data=None
    exe=True
    if name:
        user = User.objects.get(username=name)
        if user:
            exe = False
            followers = user.followers.all()
            data ={
                "user":name,
                "following":user.following.all().count(),
                "followers": followers.count(),#user.followers.all(),
                "is_foll":  request.user in followers,
                'pk':user.pk
            }      
            if request.user.username== name:
                data['is_foll']=-1
            posts = post.objects.filter(user=user.pk).reverse()
            posts_list = list(posts)  # Convert the QuerySet to a list
    paginator = Paginator(posts_list,10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, "network/index.html",{
        'page_obj':page_obj,
        "exe":exe,
        'data':data,
        
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
            request.session['no']=1
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
@csrf_exempt
def add(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("conten")
        if content=="":
            return JsonResponse({'message':"sorry content not should be void"},status=404)
        user = request.user
        pos = post(user=user,content=content,likes=0)
        pos.save()
        return JsonResponse({'message':'sucess'},status=200)
    else:
        return JsonResponse({'message':'hello get'},status=200)
def get_posts(request):
    posts = post.objects.all().values().order_by('time').reverse()# Convert the QuerySet to a list of dicts 
    posts_list = list(posts)  # Convert the QuerySet to a list
    return JsonResponse({'post': posts_list}, safe=False, status=200)
def user(request):
    users =User.objects.values('username')
    user =[]
    for us in users:
        user.append(us['username'])
    return JsonResponse({'users':user},status=200)
def following(request):
    user = User.objects.get(pk=request.user.pk)
    following = user.following.all()
    posts=[]
    for poste in post.objects.all().order_by('time').reverse():
        if poste.user in following:
            posts.append(poste)
    
    paginator = Paginator(posts,10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, "network/index.html",{
        'page_obj':page_obj,
        "exe":False        
    })
@csrf_exempt
def like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mail_id = data.get('post_pk')
        pos = post.objects.get(pk= mail_id)
        try:
            lin = link.objects.get(c_user =request.user,post = pos)
            if lin.like:
                pos.likes -=1
            else:
                pos.likes+=1
            lin.like = not(lin.like)
        except :
            lin = link.objects.create(c_user=request.user,post=pos,comment='',like=True)
            pos.likes+=1
        finally:
            pos.save()
            lin.save()
        return JsonResponse({'message':pos.likes},status=202)
    else:
        return JsonResponse({'message':'not possible without post'},status=404)
@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        body = json.loads(request.body)
        pk = body.get('mail_id')
        text = body.get('edited_text')
        c_post = post.objects.get(pk = pk)
        c_post.content = text
        c_post.save()
        return JsonResponse({'message':'sucess'},status = 200)
    return JsonResponse({'message':'notesuceds'},status =404)
@csrf_exempt
def follow_trigger(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user = User.objects.get(pk = body.get('id'))
        p_uer = User.objects.get(pk=request.user.pk)
        if user in p_uer.following.all():
            p_uer.following.remove(user)
            message = 'Follow'
        else:
            p_uer.following.add(user)
            message= 'Un_Follow'
        p_uer.save()
        return JsonResponse({'message':message},status = 200)    
    return JsonResponse({'message':'notesuceds'},status =404)
