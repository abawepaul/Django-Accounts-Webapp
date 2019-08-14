from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from django.contrib import messages
from django.contrib.messages import get_messages

from .models import *
from jobwall.models import *
import datetime
from datetime import timedelta
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')


# Create your views here.

def home(request):
    if "id" in request.session:
        return redirect('jobwall')
    else:
        return render(request, "accounts/loginreg.html")



def reg(request):
    errors = User.objects.basic_validator(request.POST)
    # check if the errors object has anything in it
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')


    pw = bcrypt.hashpw('password'.encode(), bcrypt.gensalt()).decode()
    if request.method =="POST":
        user = User.objects.create(
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            email=request.POST['email'],
            password=pw        
        )
    request.session["id"] = user.id
    request.session["fname"] = user.fname
    request.session["lname"] = user.lname
    return redirect('jobwall')


def login(request):
    try:
        user = User.objects.get(email=request.POST["email"])

        if len(request.POST['email']) < 1:
            messages.add_message(request,messages.ERROR, 'email is at least 1')
        if (not EMAIL_REGEX.match(request.POST['email'])):
            messages.add_message(request,messages.ERROR, 'email is not valid')
        if len(request.POST['password']) < 8:
            messages.add_message(request,messages.ERROR, 'pw is at least 8')


        if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
            request.session["id"] = user.id
            request.session["fname"] = user.fname
            print(user.id)
            print(user.fname)
            return redirect('jobwall')
        else:
            print("invalid values!")
            return redirect('home')
    except:
        print("boom")
        if len(request.POST['email']) < 1:
            messages.add_message(request,messages.ERROR, 'email is at least 1|')
        if (not EMAIL_REGEX.match(request.POST['email'])):
            messages.add_message(request,messages.ERROR, 'email is not valid|')
        if len(request.POST['password']) < 8:
            messages.add_message(request,messages.ERROR, 'pw is at least 8|')
        return redirect('home')

def userjobs(request, num):
    userw = job.objects.filter(postedby_id=num)


    context = {
        'user_jobs':userw

    }
    return render(request, "accounts/userjobs.html", context)




def accountedit(request,num):
    return render(request, 'accounts/accountedit.html')


def accountupdate(request):
    if request.method =="POST":
        if len(request.POST['fname']) < 2:
            messages.add_message(request,messages.ERROR, 'first name is at least 2')
        if len(request.POST['lname']) < 2:
            messages.add_message(request,messages.ERROR, 'last name is at least 2')
        if len(request.POST['email']) < 1:
            messages.add_message(request,messages.ERROR, 'email is at least 1')
        if (not NAME_REGEX.match(request.POST['fname'])):
            messages.add_message(request,messages.ERROR, 'first name invalid')
        if (not NAME_REGEX.match(request.POST['lname'])):
            messages.add_message(request,messages.ERROR, 'last name invalid')
        if (not EMAIL_REGEX.match(request.POST['email'])):
            messages.add_message(request,messages.ERROR, 'email is not valid')
        


        e = User.objects.get(id=request.session["id"])
        e.fname = request.POST['fname']
        e.lname=request.POST['lname']
        e.email=request.POST['email']
        e.save()
        return redirect('jobwall')


