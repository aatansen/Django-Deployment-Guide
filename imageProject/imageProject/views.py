from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from imageApp.models import *

def logout_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@logout_required
def signup(request):
    if request.method == "POST":
        user=CustomUserModel.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        user.save()
        return redirect('signin')
    return render(request,'signup.html')

@logout_required
def signin(request):
    if request.method=="POST":
        user=authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            login(request,user)
            return redirect('dashboard')
    return render(request,'signin.html')

@login_required
def dashboard(request):
    return render(request,'dashboard.html')

@login_required
def logoutpage(request):
    logout(request)
    return redirect('signin')

@login_required
def adduser(request):
    if request.method=="POST":
        name=request.POST.get('name')
        profile_image=request.FILES.get('profile_image')
        
        useradd=UserModel.objects.create(
            created_by=request.user,
            name=name,
            profile_image=profile_image,
        )
        useradd.save()
        return redirect('index')
    return render(request,'adduser.html')

@login_required
def index(request):
    useradd=UserModel.objects.all()
    userDict={
        'useradd':useradd,
    }
    return render(request,'index.html',userDict)

@login_required
def deleteuser(request,userid):
    userdel=UserModel.objects.get(id=userid)
    userdel.delete()
    return redirect('index')