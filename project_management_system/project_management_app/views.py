from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from project_management_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,authenticate,logout
import json
import requests
from django.contrib import messages




# Create your views here.
def showlogin(request):
    return render(request,'login_page.html')



def doLogin(request):
    if request.method!='POST':
        return HttpResponse("<h1>method no</h1>")
    else:
        
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!= None:
            login(request,user)
            if user.user_type=="1":
               return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect('/department_home')
            else:
                return HttpResponseRedirect('/employee_home')
        else:
            messages.error(request,'Invalid Login Details')
            return HttpResponseRedirect("/")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")