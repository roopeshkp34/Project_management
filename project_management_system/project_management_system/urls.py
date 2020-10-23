"""project_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from project_management_system import settings
from project_management_app import views,MdViews,EmpViews,DepViews

urlpatterns = [

    #Admin views

    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.showlogin,name="showlogin"),
    path('doLogin',views.doLogin,name="do_login"),
    path('logout_user',views.logout_user,name="logout_user"),

    path('admin_home',MdViews.admin_home,name="admin_home"),
    path('add_employee',MdViews.add_employee,name="add_employee"),
    path('add_employee_save',MdViews.add_employee_save,name="add_employee_save"),
    path('add_departmentname',MdViews.add_departmentname,name="add_departmentname"),
    path('add_departmentname_save',MdViews.add_departmentname_save,name="add_departmentname_save"),

    path('add_project',MdViews.add_project,name="add_project"),
    path('add_project_save',MdViews.add_project_save,name="add_project_save"),

    path('md_employee_add_project',MdViews.md_employee_add_project,name="md_employee_add_project"),
    path('md_save_employee_project',MdViews.md_save_employee_project,name="md_save_employee_project"),
    path('get_employeess',MdViews.get_employeess,name="get_employeess"),
    

    path('manage_session',MdViews.manage_session,name="manage_session"),
    path('add_session_save',MdViews.add_session_save,name="add_session_save"),
    path('edit_session/<str:session_year_id>',MdViews.edit_session,name="edit_session"),


    path('manage_employee',MdViews.manage_employee,name="manage_employee"),
    path('manage_employee_sort/<str:name>',MdViews.manage_employee_sort,name="manage_employee_sort"),

    path('manage_departmentname',MdViews.manage_departmentname,name="manage_departmentname"),
    path('manage_project',MdViews.manage_project,name="manage_project"),
    path('edit_employees/<str:employee_id>',MdViews.edit_employees,name="edit_employees"),
    path('edit_employee_save',MdViews.edit_employee_save,name="edit_employee_save"),

    path('edit_project/<str:project_id>',MdViews.edit_project,name="edit_project"),
    path('edit_project_save',MdViews.edit_project_save,name="edit_project_save"),

    path('edit_departmentname/<str:departmentname_id>',MdViews.edit_departmentname,name="edit_departmentname"),
    path('edit_departmentname_save',MdViews.edit_departmentname_save,name="edit_departmentname_save"),

    path('department_feedback_message',MdViews.department_feedback_message,name="department_feedback_message"),
    path('department_feedback_message_replied',MdViews.department_feedback_message_replied,name="department_feedback_message_replied"),
    path('department_comments',MdViews.department_comments,name="department_comments"),




    path('employee_leave_view',MdViews.employee_leave_view,name="employee_leave_view"),
    path('employee_approve_leave/<str:leave_id>',MdViews.employee_approve_leave,name="employee_approve_leave"),
    path('employee_disapproved_leave/<str:leave_id>',MdViews.employee_disapproved_leave,name="employee_disapproved_leave"),

    path('admin_view_attendance',MdViews.admin_view_attendance,name="admin_view_attendance"),
    path('admin_get_attendance_dates',MdViews.admin_get_attendance_dates,name="admin_get_attendance_dates"),
    path('admin_get_attendance_employee',MdViews.admin_get_attendance_employee,name="admin_get_attendance_employee"),
    path('check_email_exist',MdViews.check_email_exist,name="check_email_exist"),
    path('check_username_exist',MdViews.check_username_exist,name="check_username_exist"),

    path('delete_employee/<employee_id>',MdViews.delete_employee,name="delete_employee"),
    path('delete_departmentname/<departmentname_id>',MdViews.delete_departmentname,name="delete_departmentname"),
    path('delete_project/<projects_id>',MdViews.delete_project,name="delete_project"),
    path('delete_session/<session_year_id>',MdViews.delete_session,name="delete_session"),


    path('admin_profile',MdViews.admin_profile,name="admin_profile"),
    path('admin_profile_save',MdViews.admin_profile_save,name="admin_profile_save"),







#Department Views
    path('department_home',DepViews.department_home,name="department_home"),
    path('department_feedback',DepViews.department_feedback,name="department_feedback"),
    path('department_feedback_save',DepViews.department_feedback_save,name="department_feedback_save"),

    path('department_comment_sent',DepViews.department_comment_sent,name="department_comment_sent"),


    path('department_apply_leave',DepViews.department_apply_leave,name="department_apply_leave"),
    path('department_apply_leave_save',DepViews.department_apply_leave_save,name="department_apply_leave_save"),

    path('department_take_attendance',DepViews.department_take_attendance,name="department_take_attendance"),
    path('get_employees',DepViews.get_employees,name="get_employees"),
    path('save_attendance_data',DepViews.save_attendance_data,name="save_attendance_data"),

    path('department_update_attendance',DepViews.department_update_attendance,name="department_update_attendance"),
    path('get_attendance_dates',DepViews.get_attendance_dates,name="get_attendance_dates"),
    path('get_attendance_employee',DepViews.get_attendance_employee,name="get_attendance_employee"),
    path('save_updateattendance_data',DepViews.save_updateattendance_data,name="save_updateattendance_data"),




    path('admin_view_project',DepViews.admin_view_project,name="admin_view_project"),

    path('employee_add_project',DepViews.employee_add_project,name="employee_add_project"),
    path('save_employee_project',DepViews.save_employee_project,name="save_employee_project"),
    path('department_view_project',DepViews.department_view_project,name="department_view_project"),


    path('department_profile',DepViews.department_profile,name="department_profile"),
    path('department_profile_save',DepViews.department_profile_save,name="department_profile_save"),








#Employee Views
    path('employee_home',EmpViews.employee_home,name="employee_home"),
    path('employee_apply_leave',EmpViews.employee_apply_leave,name="employee_apply_leave"),
    path('employee_apply_leave_save',EmpViews.employee_apply_leave_save,name="employee_apply_leave_save"),

    path('employee_feedback',EmpViews.employee_feedback,name="employee_feedback"),
    path('employee_feedback_save',EmpViews.employee_feedback_save,name="employee_feedback_save"),
    path('employee_comments',EmpViews.employee_comments,name="employee_comments"),


    path('employee_view_attendence',EmpViews.employee_view_attendence,name="employee_view_attendence"),
    path('employee_view_attendence_post',EmpViews.employee_view_attendence_post,name="employee_view_attendence_post"),

    path('employee_profile',EmpViews.employee_profile,name="employee_profile"),
    path('employee_profile_save',EmpViews.employee_profile_save,name="employee_profile_save"),

    path('employee_view_project',EmpViews.employee_view_project,name="employee_view_project"),
    path('employee_compleate_project/<str:projects_id>',EmpViews.employee_compleate_project,name="employee_compleate_project"),
    path('employee_incompleate_project/<str:projects_id>',EmpViews.employee_incompleate_project,name="employee_incompleate_project"),



]
# ]+static(settings.MEDIA_URL,doccument_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,doccument_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)