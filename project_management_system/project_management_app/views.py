from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from project_management_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,authenticate,logout
import requests
import json
from django.contrib import messages




# Create your views here.
def showlogin(request):
    return render(request,'login_page.html')



def doLogin(request):
    if request.method!='POST':
        return HttpResponse("<h1>method no</h1>")
    else:
        # captcha_token=request.POST.get("g-recaptcha-response") 
        # cap_url="https://www.google.com/recaptcha/api/siteverify"
        # cap_secret="6LctodEZAAAAANh_vMbCzXcMGCy2qARYsKsICzox"
        # cap_data={"secret":cap_secret,"response":captcha_token}
        # cap_server_response=requests.post(url=cap_url,data=cap_data)
        # cap_json=json.loads(cap_server_response.text)
        # if cap_json['success']==False:
        #     messages.error(request,'Invalid Captcha Try Again')
        #     return HttpResponseRedirect("/")
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