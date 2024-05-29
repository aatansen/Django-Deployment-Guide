from django.shortcuts import render,redirect
from imageApp.models import *


def adduser(request):
    if request.method=="POST":
        name=request.POST.get('name')
        profile_image=request.FILES.get('profile_image')
        
        useradd=UserModel.objects.create(
            name=name,
            profile_image=profile_image,
        )
        useradd.save()
        return redirect('index')
    return render(request,'adduser.html')

def index(request):
    useradd=UserModel.objects.all()
    userDict={
        'useradd':useradd,
    }
    return render(request,'index.html',userDict)
