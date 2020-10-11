from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse

class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "project_management_app.MdViews":
                    pass
                elif modulename == "project_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("admin_home")

            elif user.user_type == "2":
                if modulename == "project_management_app.DepViews":
                    pass
                elif modulename == "project_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("department_home")

            elif user.user_type == "3":
                if modulename == "project_management_app.EmpViews":
                    pass
                elif modulename == "project_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("employee_home")
            else:
                return redirect("showLoginPage")

                
        else:
            if request.path == reverse("showlogin") or request.path == reverse("do_login") or modulename == "django.contrib.auth.views":
                pass
            else:
                return redirect("showlogin")
