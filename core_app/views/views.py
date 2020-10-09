# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from core_app.email_backend import EmailBackEnd


def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(
            request, 
            username=request.POST.get('email'), 
            password=request.POST.get('password')
        )
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('principal_home')
                
            elif user_type == '2':
                return redirect('teacher-home')
                
            elif user_type == '3':
                return redirect('student-home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


