from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from project_management_app.models import DepartmentName,Comment,ProjectImages,EmployeeProject,EmployeeProjectImages,SessionYearModel,Attendence,CustomUser,Employee,FeedBackEmployee,LeaveReportEmployee,Projects,AttendenceReport
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.files.storage import FileSystemStorage
from django.db.models import Count


def department_home(request):
    #fetch all employees
    employee_obj=Employee.objects.get(admin=request.user.id)
    departmentname=DepartmentName.objects.get(id=employee_obj.departmentname_id.id)
    projects=Projects.objects.filter(departmentname_id=departmentname)
    departmentname_id_list=[]
    for project in projects:
        departmentname=DepartmentName.objects.get(id=project.departmentname_id.id)
        departmentname_id_list.append(departmentname.id)

    final_departmentname=[]
    #removing duplicate departmentname id
    for departmentname_id in departmentname_id_list:
        if departmentname_id not in final_departmentname:
            final_departmentname.append(departmentname_id)
    # employee_count=Employee.objects.filter(departmentname_id__in=final_departmentname).count()
    employee_count=Employee.objects.filter(category='Employee',departmentname_id__in=final_departmentname).count()


    #fetch all attendance count
    attendance_count=Attendence.objects.filter(projects_id__in=projects).count()

    #fetch all Approve Leave count
    department=Employee.objects.get(admin=request.user.id)
    leave_count=LeaveReportEmployee.objects.filter(employee_id=department.id,leave_status=1).count()
    project_count=projects.count()

    #fetch Attendance data by Project
    project_list=[]
    attendance_list=[]
    for project in projects:
        attendance_count1=Attendence.objects.filter(projects_id=project.id).count()
        project_list.append(project.project_name)
        attendance_list.append(attendance_count1)

    employee_attendance=Employee.objects.filter(category='Employee',departmentname_id__in=final_departmentname)
    employee_list=[]
    employee_list_attendance_present=[]
    employee_list_attendance_absent=[]

    for employee in employee_attendance:
        attendance_present_count=AttendenceReport.objects.filter(status=True,employee_id=employee.id).count()
        attendance_absent_count=AttendenceReport.objects.filter(status=False,employee_id=employee.id).count()
        employee_list.append(employee.admin.username)
        employee_list_attendance_present.append(attendance_present_count)
        employee_list_attendance_absent.append(attendance_absent_count)
    context = {
        "employee_count":employee_count,
        "attendance_count":attendance_count,
        "leave_count":leave_count,
        "project_count":project_count,
        "project_list":project_list,
        "attendance_list":attendance_list,
        "employee_list":employee_list,
        "present_list":employee_list_attendance_present,
        "absent_list":employee_list_attendance_absent
    }

    


    return render(request,"department_template/department_home_template.html",context)


def department_take_attendance(request):
    employee=Employee.objects.get(admin=request.user.id)
    departmentname=employee.departmentname_id
    projects=Projects.objects.filter(departmentname_id=departmentname)
    session_year=SessionYearModel.objects.all()
    today=date.today()
    d1 = today.strftime("%d/%m/%Y")
    print(d1)
    return render(request,"department_template/department_take_attendance.html",{"projects":projects,"session_year":session_year,"d1":d1})


@csrf_exempt
def get_employees(request):
    project_id=request.POST.get("project")
    session_year=request.POST.get("session_year")
    print(project_id)
    project=Projects.objects.get(id=project_id)
    session_model=SessionYearModel.objects.get(id=session_year)
    employees=Employee.objects.filter(departmentname_id=project.departmentname_id,session_year_id=session_model)
    list_data=[]
    for employee in employees:
        if employee.category=="Employee":
            data_small={"id":employee.admin.id,"name":employee.admin.first_name}
            list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def save_attendance_data(request):
    employee_ids=request.POST.get("employee_ids")
    project_id=request.POST.get("project_id")
    attendence_date=request.POST.get("attendence_date")
    session_year_id=request.POST.get("session_year_id")

    project_model=Projects.objects.get(id=project_id)
    session_model=SessionYearModel.objects.get(id=session_year_id)
    json_employee=json.loads(employee_ids)
    try:
        attendance=Attendence(projects_id=project_model,attendence_date=attendence_date,session_year_id=session_model)
        attendance.save()

        for emp in json_employee:
            employee=Employee.objects.get(admin=emp['id'])
            attendance_report=AttendenceReport(employee_id=employee,attendence_id=attendance,status=emp['status'])
            attendance_report.save()
        return HttpResponse("OK")

    except:
        return HttpResponse("ERROR")


def department_update_attendance(request):
    employee=Employee.objects.get(admin=request.user.id)
    departmentname=employee.departmentname_id
    projects=Projects.objects.filter(departmentname_id=departmentname)
    session_year_id=SessionYearModel.objects.all()
    return render(request,"department_template/department_update_attendance.html",{"projects":projects,"session_year_id":session_year_id})


@csrf_exempt
def get_attendance_dates(request):
    project=request.POST.get("project")
    session_year_id=request.POST.get("session_year_id")
 
    project_obj=Projects.objects.get(id=project)
    session_year_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance=Attendence.objects.filter(projects_id=project_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendence_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)



@csrf_exempt
def get_attendance_employee(request):
   
    attendance_date=request.POST.get("attendence_date")

    attendance=Attendence.objects.get(id=attendance_date)

    attendance_data=AttendenceReport.objects.filter(attendence_id=attendance)
    list_data=[]
    for employee in attendance_data:
        data_small={"id":employee.employee_id.admin.id,"name":employee.employee_id.admin.first_name+"  "+employee.employee_id.admin.last_name,"status":employee.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def save_updateattendance_data(request):
    employee_ids=request.POST.get("employee_ids")
    # project_id=request.POST.get("project_id")
    attendence_date=request.POST.get("attendence_date")
    attendance=Attendence.objects.get(id=attendence_date)

    json_employee=json.loads(employee_ids)
    try:
        for emp in json_employee:
            employee=Employee.objects.get(admin=emp['id'])
            attendance_report=AttendenceReport.objects.get(employee_id=employee,attendence_id=attendance)
            attendance_report.status=emp['status']
            attendance_report.save()
        return HttpResponse("OK")

    except:
        return HttpResponse("ERROR")


def department_apply_leave(request):
    department_obj=Employee.objects.get(admin=request.user.id)
    leave_date=LeaveReportEmployee.objects.filter(employee_id=department_obj)
    return render(request,"department_template/department_apply_leave.html",{"leave_date":leave_date})



def department_apply_leave_save(request):
    if request.method!='POST':
        return redirect("department_apply_leave")

    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_reason")

        department_obj=Employee.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportEmployee(employee_id=department_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied For Leave")
            return redirect('/department_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave!")
            return redirect('/department_apply_leave')



def department_feedback(request):
    department_id=Employee.objects.get(admin=request.user.id)
    feedback_data=FeedBackEmployee.objects.filter(employee_id=department_id).order_by('-id')
    return render(request,"department_template/department_feedback.html",{"feedback_data":feedback_data})



def department_feedback_save(request):
    if request.method!='POST':
        return redirect("department_feedback")

    else:
        feedback_msg=request.POST.get("feedback_msg")

        department_obj=Employee.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackEmployee(employee_id=department_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return redirect('/department_feedback')
        except:
            messages.error(request, "Failed to Sent Feedback!")
            return redirect('/department_feedback')



def department_comment_sent(request):
    department_id=Employee.objects.get(admin=request.user.id)
    comments=Comment.objects.filter(employee_id=department_id,reply=None).order_by('-id')
    department_obj=Employee.objects.get(admin=request.user.id)

    if request.method=='POST':
        content=request.POST.get("content")
        reply_id=request.POST.get("comment_id")
        comment_qs=None
        if reply_id:
            comment_qs=Comment.objects.get(id=reply_id)
        try:
            comment=Comment.objects.create(content=content,employee_id=department_obj,reply=comment_qs)
            comment.save()
            return redirect('/department_comment_sent')
        except:
            messages.error(request, "Failed to Sent Feedback!")
            return redirect('/department_comment_sent')

    
    return render(request,"department_template/department_comments.html",{"comments":comments})



def admin_view_project(request):
    employee=Employee.objects.get(admin=request.user.id)
    departmentname=employee.departmentname_id
    project=Projects.objects.filter(departmentname_id=departmentname)
    list=[]
    for projec in project:
        project_fil=ProjectImages.objects.filter(project_id=projec)
        list.append(project_fil)
    context = {
        "project": project,
        "list":list,
        
    }
    
    return render(request,"department_template/admin_view_project.html",context)



def employee_add_project(request):
    employee=Employee.objects.get(admin=request.user.id)
    departmentname=employee.departmentname_id
    projects=Projects.objects.filter(departmentname_id=departmentname)
    session_year=SessionYearModel.objects.all()
    return render(request,"department_template/add_project_template.html",{"projects":projects,"session_year":session_year})  



def save_employee_project(request):
    if request.method!='POST':
        return redirect("employee_add_project")
    else:
        employee_admin_id=request.POST.get("employee_list")
        project_details=request.POST.get("project_details")
        project_id=request.POST.get("project")
        images=request.FILES.getlist("file[]")



        employee_obj=Employee.objects.get(admin=employee_admin_id)
        project_obj=Projects.objects.get(id=project_id)
        
        try:
            check_exist=EmployeeProject.objects.filter(projects_id=project_obj,employee_id=employee_obj).exists()
            if check_exist:
                add_project=EmployeeProject.objects.get(projects_id=project_obj,employee_id=employee_obj)
                add_project.project_details=project_details
                add_project.save()
                messages.success(request, "Project Updating  Successfully!")
                return redirect('/employee_add_project')
            else:
                add_project=EmployeeProject(employee_id=employee_obj,projects_id=project_obj,project_details=project_details)
                add_project.save()
                for img in images:
                    fs=FileSystemStorage()
                    file_path=fs.save(img.name,img)
                    pimage=EmployeeProjectImages(empproject_id=add_project,image=file_path)
                    pimage.save()
                messages.success(request, "Project Senting  Successfully!")
                return redirect('/employee_add_project')
        except:
            messages.error(request, "Failed to Sent Project")
            return redirect('/employee_add_project')



def department_view_project(request):
    employee_project=EmployeeProjectImages.objects.all()
    list=[]
    return render(request,"department_template/view_project_history.html",{"employee_project":employee_project})
    


def department_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"department_template/department_profile.html",{"user":user})


def department_profile_save(request):
    if request.method!='POST':
        return redirect("department_profile")
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
            return redirect('/department_profile')
        except:
            messages.error(request, "Failed to Update Profile!")
            return redirect('/department_profile')