from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from imageApp.models import *
from imageApp.forms import *



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
        form_data=RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,'register success')
            return redirect('signin')
    else:
        form_data=RegisterForm()

    context={
        'form_title':'Signup Page',
        'form_btn':'Signup',
        'form_data':form_data,
        'redirect_url':'signin',
        'redirect_text':'Already have an acccount?'
    }

    return render(request, 'master/base-form.html',context=context)


@logout_required
def signin(request):
    if request.method == "POST":
        form_data=LoginForm(request,request.POST)
        if form_data.is_valid():
            user=form_data.get_user()
            login(request,user)
            messages.success(request,'login success')
            return redirect('dashboard')
    else:
        form_data=LoginForm()

    context={
        'form_title':'Signin Page',
        'form_btn':'Signin',
        'form_data':form_data,
        'redirect_url':'signup',
        'redirect_text':'Dont have an acccount?'
    }
    return render(request, 'master/base-form.html',context=context)


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def signout(request):
    logout(request)
    return redirect('signin')


@login_required
def adduser(request):
    if request.method == "POST":
        form_data=UserForm(request.POST,request.FILES)
        if form_data.is_valid():
            form_data=form_data.save(commit=False)
            form_data.created_by=request.user
            form_data.save()
            messages.success(request,'user add success')
            return redirect('users')

    else:
        form_data=UserForm()

    context={
        'form_title':'Add user Page',
        'form_btn':'Add user',
        'form_data':form_data,
    }
    return render(request, 'master/base-form.html',context=context)


@login_required
def users(request):
    users = UserModel.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'users.html', context=context)

@login_required
def deleteuser(request, id):
    userdel = UserModel.objects.get(id=id)
    userdel.delete()
    return redirect('users')
