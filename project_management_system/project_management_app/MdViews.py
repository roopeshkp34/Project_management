from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.files.storage import FileSystemStorage
from project_management_app.models import DepartmentName,EmployeeProject,EmployeeProjectImages,Comment,ProjectImages,SessionYearModel,CustomUser,Employee,Attendence,AttendenceReport,Projects,FeedBackEmployee,LeaveReportEmployee


def admin_home(request):
    employee_count=Employee.objects.all().count()
    department_count=Employee.objects.filter(category="Hod").count()
    departmentname_count=DepartmentName.objects.all().count()
    project_count=Projects.objects.all().count()


    departmentname_all=DepartmentName.objects.all()
    departmentname_list=[]
    project_count_list=[]
    employee_count_list_in_departmentname=[]
    for departmentname in departmentname_all:
        projects=Projects.objects.filter(departmentname_id=departmentname.id).count()
        employees=Employee.objects.filter(departmentname_id=departmentname.id).count()
        departmentname_list.append(departmentname.department_name)
        project_count_list.append(projects)

        employee_count_list_in_departmentname.append(employees)

    projects_all=Projects.objects.all()
    project_list=[]
    employee_count_list_in_project=[]
    for project in projects_all:
        departmentname=DepartmentName.objects.get(id=project.departmentname_id.id)
        employee_count1=Employee.objects.filter(departmentname_id=departmentname.id).count()
        project_list.append(project.project_name)
        employee_count_list_in_project.append(employee_count1)


    return render(request,"md_template/home_content.html",{"employee_count":employee_count,"department_count":department_count,"departmentname_count":departmentname_count,"project_count":project_count,"departmentname_list":departmentname_list,"project_count_list":project_count_list,"employee_count_list_in_departmentname":employee_count_list_in_departmentname,"project_list":project_list,"employee_count_list_in_project":employee_count_list_in_project})


def add_employee(request):
    departmentname=DepartmentName.objects.all()
    sessions=SessionYearModel.objects.all()
    return render(request,'md_template/add_employee_template.html',{"departmentname":departmentname,"sessions":sessions})

 
def add_employee_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_employee')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        session_year_id=request.POST.get('sessions')
        departmentname_id=request.POST.get('department_name')
        gender=request.POST.get('gender')
        category=request.POST.get("category")

        # profile_pic=request.FILES['profile_pic']
        # fs=FileSystemStorage()
        # filename=fs.save(profile_pic.name,profile_pic)
        # profile_pic_url=fs.url(filename)

        try:
            if category == "Employee":
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                user.employee.address = address
                departmentname_obj=DepartmentName.objects.get(id=departmentname_id)
                user.employee.departmentname_id=departmentname_obj
                sesson_year=SessionYearModel.objects.get(id=session_year_id)
                user.employee.session_year_id=sesson_year
                user.employee.gender=gender
                user.employee.category=category
                # user.employee.profile_pic=profile_pic_url
                user.save()
                messages.success(request, "Employee Added Successfully!")
                return redirect('/add_employee')
            else:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
                user.employee.address = address
                departmentname_obj=DepartmentName.objects.get(id=departmentname_id)
                user.employee.departmentname_id=departmentname_obj
                sesson_year=SessionYearModel.objects.get(id=session_year_id)
                user.employee.session_year_id=sesson_year
                user.employee.gender=gender
                user.employee.category=category
                # user.employee.profile_pic=profile_pic_url
                user.save()
                messages.success(request, "Employee Added Successfully!")
                return redirect('/add_employee')
        except:
            messages.error(request, "Failed to Add Employye!")
            return redirect('/add_employee')



def add_departmentname(request):
    return render(request,"md_template/add_departmentname_template.html")


def add_departmentname_save(request):
    if request.method!='POST':
        return redirect("Method Not Allowed")
    else:
        department_name=request.POST.get('department_name')
        try:
            department_name_model=DepartmentName(department_name=department_name)
            department_name_model.save()
            messages.success(request, "Successfully Added New Department!")
            return redirect('/add_departmentname')
        except:
            messages.error(request, "Failed to Add Department!")
            return redirect('/add_departmentname')



def add_project(request):
    departmentname=DepartmentName.objects.all()
    department=Employee.objects.filter(category='Hod')
    context = {
        "department": department,
        "departmentname": departmentname
    }
    return render(request,"md_template/add_project_template.html",context)


def add_project_save(request):
    if request.method!='POST':
        messages.error(request, "Invalid Method ")
        return redirect('add_project')
    else:
        project_name=request.POST.get("project_name")
        project_details=request.POST.get("project_details")
        departmentname_id=request.POST.get("department_name")
        departmentname=DepartmentName.objects.get(id=departmentname_id)
        department_id=request.POST.get("department")
        images=request.FILES.getlist("file[]")
        department=Employee.objects.get(id=department_id)
        try:
            projects=Projects(project_name=project_name,departmentname_id=departmentname,employee_id=department,project_details=project_details)
            projects.save()
            for img in images:
                fs=FileSystemStorage()
                file_path=fs.save(img.name,img)
                pimage=ProjectImages(project_id=projects,image=file_path)
                pimage.save()

            messages.success(request, "Project Added Successfully!")
            return redirect('/add_project')
        except:
            messages.error(request, "Failed to Add Project!")
            return redirect('/add_project')



def md_employee_add_project(request):
    departmentname=DepartmentName.objects.all()
    
    return render(request,"md_template/md_add_project_template.html",{"departmentname":departmentname})  



def md_save_employee_project(request):
    if request.method!='POST':
        return redirect("md_employee_add_project")
    else:
        project_name=request.POST.get("project_name")
        project_details=request.POST.get("project_details")
        departmentname_id=request.POST.get("department_name")
        departmentname=DepartmentName.objects.get(id=departmentname_id)
        department_id=request.POST.get("department")
        images=request.FILES.getlist("file[]")
        department=Employee.objects.get(admin=department_id)
        
        try:
            projects=Projects(project_name=project_name,departmentname_id=departmentname,employee_id=department,project_details=project_details)
            projects.save()
            for img in images:
                fs=FileSystemStorage()
                file_path=fs.save(img.name,img)
                pimage=ProjectImages(project_id=projects,image=file_path)
                pimage.save()
            messages.success(request, "Project Senting  Successfully!")
            return redirect('/md_employee_add_project')
        except:
            messages.error(request, "Failed to Sent Project")
            return redirect('/md_employee_add_project')
@csrf_exempt
def get_employeess(request):
    department_name=request.POST.get("department_name")
    department_id=DepartmentName.objects.get(id=department_name)
    employees=Employee.objects.filter(departmentname_id=department_id)
    list_data=[]
    for employee in employees:
        if employee.category=="Hod":
            data_small={"id":employee.admin.id,"name":employee.admin.first_name+"  "+employee.admin.last_name}
            list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)





def manage_session(request):
    return render(request,"md_template/manage_session_template.html")



def add_session_save(request):
    if request.method!="POST":
        return redirect("manage_session")
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")
        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Added Successfully!")
            return redirect('/manage_session')
        except:
            messages.error(request, "Failed to Add Session!")
            return redirect('/manage_session')


def manage_employee(request):
    employee=Employee.objects.all()
    session=SessionYearModel.objects.all()
    context = {
        "employee": employee,
        "session":session,
        
    }
    return render(request,"md_template/manage_employee_template.html",context)


def manage_employee_sort(request,name):
    employee=Employee.objects.all()
    session=SessionYearModel.objects.all()
    context = {
        "employee": employee,
        "session":session,
        "filter":name
        
    }
    return render(request,"md_template/manage_employee_sort_template.html",context)

def manage_departmentname(request):
    departmentname=DepartmentName.objects.all()
    context = {
        "departmentname": departmentname,
        
    }
    return render(request,"md_template/manage_departmentname_template.html",context)



def manage_project(request):
    project=Projects.objects.all()
    list=[]
    for projec in project:
        project_fil=ProjectImages.objects.filter(project_id=projec)
        list.append(project_fil)
    context = {
        "project": project,
        "list":list,
        
    }
    
    return render(request,"md_template/manage_project_template.html",context)



def edit_employees(request,employee_id):
    employees=Employee.objects.get(admin=employee_id)
    departmentname=DepartmentName.objects.all()
    session_years=SessionYearModel.objects.all()
    employee=Employee.objects.values('category').distinct()
    context = {
        "employees": employees,
        "departmentname": departmentname,
        "id":employee_id,
        "session_years":session_years,
        "employee":employee
    }
    return render(request,"md_template/edit_employee_template.html",context)




def edit_employee_save(request):
    if request.method!='POST':
        messages.error(request, "Invalid Method ")
        return redirect('edit_employees')
    else:
        employee_id=request.POST.get("employee_id")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        session_year_id=request.POST.get('session_year')
        departmentname_id=request.POST.get('department_name')
        gender=request.POST.get('gender')
        category=request.POST.get("category")

        

        # if request.FILES.get('profile_pic',False):
        #     profile_pic=request.FILES['profile_pic']
        #     fs=FileSystemStorage()
        #     filename=fs.save(profile_pic.name,profile_pic)
        #     profile_pic_url=fs.url(filename)
        # else:
        #     profile_pic_url=None
        try:
            if category == "Employee":
                user=CustomUser.objects.get(id=employee_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.user_type=3
                user.save()
            
                employee=Employee.objects.get(admin=employee_id)
                employee.address=address
                session_year=SessionYearModel.objects.get(id=session_year_id)
                employee.session_year_id=session_year
                employee.gender=gender
                departmentname=DepartmentName.objects.get(id=departmentname_id)
                employee.departmentname_id=departmentname
                employee.category=category
                # employee.profile_pic=profile_pic_url
                employee.save()
                messages.success(request, "Employee Edited Successfully!")
                return redirect('/edit_employees/'+employee_id)
            else:
                user=CustomUser.objects.get(id=employee_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.user_type=2
                user.save()
            
                employee=Employee.objects.get(admin=employee_id)
                employee.address=address
                session_year=SessionYearModel.objects.get(id=session_year_id)
                employee.session_year_id=session_year
                employee.gender=gender
                departmentname=DepartmentName.objects.get(id=departmentname_id)
                employee.departmentname_id=departmentname
                employee.category=category
                # employee.profile_pic=profile_pic_url
                employee.save()
                messages.success(request, "Employee Edited Successfully!")
                return redirect('/edit_employees/'+employee_id)
        except:
            messages.error(request, "Failed to Edit Employee!")
            return redirect('/edit_employees/'+employee_id)



def edit_departmentname(request,departmentname_id):
    
    hod=Employee.objects.filter(departmentname_id=departmentname_id)
    departmentname=DepartmentName.objects.get(id=departmentname_id)
    return render(request,"md_template/edit_departmentname_template.html",{"departmentname" : departmentname,"id":id,"hod":hod})




def edit_departmentname_save(request):
    if request.method!='POST':
        messages.error(request, "Invalid Method ")
        return redirect('edit_employees')
    else:
        departmentname_id=request.POST.get("departmentname_id")
        # employee_id=request.POST.get("employee_id")

        department_name=request.POST.get("department_name")
        department=request.POST.get("hod")

        try:
            departmentname=DepartmentName.objects.get(id=departmentname_id)
            departmentname.department_name=department_name
            departmentname.save()
            department=Employee.objects.get(id=department)
            department.category='Hod'
            department.save()
            messages.success(request, "Department Name Edited Successfully!")
            return redirect('/edit_departmentname/'+departmentname_id)
        except:
            messages.error(request, "Failed to Edit Department Name!")
            return redirect('/edit_departmentname/'+departmentname_id)



def edit_project(request,project_id):
    project=Projects.objects.get(id=project_id)
    departmentname=DepartmentName.objects.all()
    department=Employee.objects.filter(category='Hod')
    project=Projects.objects.get(id=project_id)
    return render(request,"md_template/edit_project_template.html",{"project":project,"departmentname":departmentname,"department":department,"id":project_id})



def edit_project_save(request):
    if request.method!='POST':
        messages.error(request, "Invalid Method ")
        return redirect('edit_project')
    else:
        project_id=request.POST.get("project_id")
        project_name=request.POST.get("project_name")
        project_details=request.POST.get("project_details")
        department_id=request.POST.get("department")
        departmentname_id=request.POST.get("department_name")
        try:
            project=Projects.objects.get(id=project_id)
            project.project_name=project_name
            project.project_details=project_details
            department=CustomUser.objects.get(id=department_id)
            project.department_id=department
            departmentname=DepartmentName.objects.get(id=departmentname_id)
            project.departmentname_id=departmentname
            project.save()
            messages.success(request, "Project Edited Successfully!")
            return redirect('/edit_project/'+project_id)
        except:
            messages.error(request, "Failed to Edit Project!")
            return redirect('/edit_project/'+project_id)



def department_feedback_message(request):
    feedbacks=FeedBackEmployee.objects.all()
    # user=Employee.objects.all()
    return render(request,"md_template/department_feedback_template.html",{"feedbacks":feedbacks})


@csrf_exempt
def department_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")
    try:
        feedback=FeedBackEmployee.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()

        return HttpResponse("True")
    except:
        return HttpResponse("True")  


def department_comments(request):
    comments=Comment.objects.filter(reply=None).order_by('-id')

    if request.method=='POST':
        content=request.POST.get("content")
        reply_id=request.POST.get("comment_id")
        comment_qs=None
        if reply_id:
            comment_qs=Comment.objects.get(id=reply_id)

        comment=Comment.objects.create(content=content,reply=comment_qs)
        comment.save()
        return redirect('/department_comments')

    
    return render(request,"md_template/department_comments.html",{"comments":comments})


def employee_leave_view(request):
    leaves=LeaveReportEmployee.objects.all()
    return render(request,"md_template/employee_leave_view.html",{"leaves":leaves})


def employee_approve_leave(request,leave_id):
    leave=LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return redirect("employee_leave_view")
    

def employee_disapproved_leave(request,leave_id):
    leave=LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return redirect("employee_leave_view")


def admin_view_attendance(request):
    projects=Projects.objects.all()
    session_year_id=SessionYearModel.objects.all()
    return render(request,"md_template/admin_view_attendance.html",{"projects":projects,"session_year_id":session_year_id})



@csrf_exempt
def admin_get_attendance_dates(request):
    project=request.POST.get("project")
    session_year_id=request.POST.get("session_year_id")

    project_obj=Projects.objects.get(id=project)
    session_year_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance=Attendence.objects.filter(projects_id=project_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendence_date":str(attendance_single.attendence_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def admin_get_attendance_employee(request):
    attendance_date=request.POST.get("attendence_date")

    attendance=Attendence.objects.get(id=attendance_date)

    attendance_data=AttendenceReport.objects.filter(attendence_id=attendance)
    list_data=[]
    for employee in attendance_data:
        data_small={"id":employee.employee_id.admin.id,"name":employee.employee_id.admin.first_name+"  "+employee.employee_id.admin.last_name,"status":employee.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)



@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse("True")
    else:
        return HttpResponse("False")



@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse("True")
    else:
        return HttpResponse("False")



def delete_employee(request,employee_id):
    employee=Employee.objects.get(admin=employee_id)
    employee.delete()
    return redirect("manage_employee")


def delete_departmentname(request,departmentname_id):
    departmentname=DepartmentName.objects.get(id=departmentname_id)
    departmentname.delete()
    return redirect("manage_departmentname")


def delete_project(request,projects_id):
    project=Projects.objects.get(id=projects_id)
    project.delete()
    return redirect("manage_project")


def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"md_template/admin_profile.html",{"user":user})


def admin_profile_save(request):
    if request.method!='POST':
        return redirect("admin_profile")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("change_password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect('/admin_profile')
        except:
            messages.error(request, "Failed to Update Profile!")
            return redirect('/admin_profile')