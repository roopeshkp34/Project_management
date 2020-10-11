from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
# from django.contrib.auth.models import User

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data=((1,"MD"),(2,"HOD"),(3,"Employee"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)


class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    objects=models.Manager()


class AdminMD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    # name=models.CharField(max_length=255)
    # email=models.CharField(max_length=255)
    # password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects=models.Manager()


class DepartmentName(models.Model):
    id=models.AutoField(primary_key=True)
    department_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects=models.Manager()



# class Department(models.Model):
#     id=models.AutoField(primary_key=True)
#     admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     address=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at =models.DateTimeField(auto_now_add=True)
#     objects=models.Manager()
    



# class Projects(models.Model):
#     id=models.AutoField(primary_key=True)
#     project_name=models.CharField(max_length=255)
#     project_details=models.CharField(max_length=255)
#     departmentname_id=models.ForeignKey(DepartmentName,on_delete=models.CASCADE,default=1)
#     department_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at =models.DateTimeField(auto_now_add=True)
#     objects=models.Manager()


class Employee(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    # name=models.CharField(max_length=255)
    # email=models.CharField(max_length=255)
    # password=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)
    category=models.CharField(max_length=255)
    profile_pic=models.FileField()
    address=models.TextField()
    departmentname_id=models.ForeignKey(DepartmentName,on_delete=models.DO_NOTHING)
    # session_start_year=models.DateField()
    # session_end_year=models.DateField()
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects=models.Manager()


class Projects(models.Model):
    id=models.AutoField(primary_key=True)
    project_name=models.CharField(max_length=255)
    project_details=models.CharField(max_length=255)
    departmentname_id=models.ForeignKey(DepartmentName,on_delete=models.CASCADE,default=1)
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects=models.Manager()
    


class ProjectImages(models.Model):
    id=models.AutoField(primary_key=True)
    project_id=models.ForeignKey(Projects,on_delete=models.CASCADE)
    image=models.FileField(upload_to='media/collection/')
    def __str__(self):
        return self.title



class Attendence(models.Model):
    id=models.AutoField(primary_key=True)
    projects_id=models.ForeignKey(Projects,on_delete=models.DO_NOTHING)
    attendence_date=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()



class AttendenceReport(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employee,on_delete=models.DO_NOTHING)
    attendence_id=models.ForeignKey(Attendence,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()


class LeaveReportEmployee(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    status=models.IntegerField(default=0)
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()


# class LeaveReportDepartment(models.Model):
#     id=models.AutoField(primary_key=True)
#     department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
#     leave_date=models.CharField(max_length=255)
#     leave_message=models.TextField()
#     leave_status=models.IntegerField(default=0)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now_add=True)
#     objects=models.Manager()


class FeedBackEmployee(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    feedback=models.TextField()
    status=models.IntegerField(default=0)
    feedback_reply= models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()

class Comment(models.Model):
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)
    content=models.TextField(max_length=160)
    reply=models.ForeignKey('Comment',null=True,related_name='replies',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()


    def __str__(self):
        return '{}-{}'.format(str(self.user.username))



# class FeedBackDepartment(models.Model):
#     id=models.AutoField(primary_key=True)
#     department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
#     feedback=models.TextField()
#     feedback_reply=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now_add=True)
#     objects=models.Manager()


class NotificationEmployee(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()


# class NotificationDepartment(models.Model):
#     id=models.AutoField(primary_key=True)
#     department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
#     message=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now_add=True)
#     objects=models.Manager()

 




class EmployeeProject(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    projects_id=models.ForeignKey(Projects,on_delete=models.CASCADE)
    # departmentname_id=models.ForeignKey(DepartmentName,on_delete=models.CASCADE)
    project_details=models.TextField()
    project_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=models.Manager()

class EmployeeProjectImages(models.Model):
    id=models.AutoField(primary_key=True)
    empproject_id=models.ForeignKey(EmployeeProject,on_delete=models.CASCADE)
    image=models.FileField(upload_to='media/collection/')
    def __str__(self):
        return self.title


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminMD.objects.create(admin=instance)
        if instance.user_type==2:
            Employee.objects.create(admin=instance,departmentname_id=DepartmentName.objects.get(id=1),session_year_id=SessionYearModel.objects.get(id=1),address="",profile_pic="",gender="")
        if instance.user_type==3:
            Employee.objects.create(admin=instance,departmentname_id=DepartmentName.objects.get(id=1),session_year_id=SessionYearModel.objects.get(id=1),address="",profile_pic="",gender="")


@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminmd.save()
    if instance.user_type==2:
        instance.employee.save()
    if instance.user_type==3:
        instance.employee.save()