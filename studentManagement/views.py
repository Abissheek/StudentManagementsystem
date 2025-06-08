from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout,login
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib import messages


from django.contrib.auth import authenticate, login

from studentManagement import emailBackend
from studentManagement.models import CustomUser

# Create your views here.
def showDemoPage(request):
    return render(request, 'demo.html')


def showLoginPage(request):
    return render(request,'login.html')


def doLogin(request):
    if request.method!="POST":
        return HttpResponse("Error occured for method", status=405)
    
    email=request.POST.get("email","")
    password=request.POST.get("password","")

    if not email or not password:
        return HttpResponse('Email or password missing', status=400)
    user=authenticate(request, username=email, password=password)
    if user is not None:
        print("Success")
        login(request, user)
        if user.user_type=='1':
            return redirect('/admin_home')
        elif user.user_type=='2':
            return redirect("staff_home")
        else:
            return redirect("student_home")
    else:
        messages.error(request, "Invalid Login Details")
        print("Invalid")
        return HttpResponseRedirect("/")
        

# def GetUserDetails(request):
#     user=request.user
#     if user.is_authenticated:
#         return HttpResponse(f"User:{user.email},User Type:{user.user_type_display()}")
#     else:
#         return HttpResponse("Please Login First")

def LogOutUser(request):
    logout(request)
    return redirect("/")