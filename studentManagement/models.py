from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()




class CustomUser(AbstractUser):
    user_type_date=((1,"HOD"),(2,'Staffs'),(3,'Student'))
    user_type=models.CharField(default=1,choices=user_type_date,max_length=50)


class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)




class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=200)
    course_id=models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    staff_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()



class Student(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=200)
    profile_pic=models.FileField(null=True,blank=True)
    address=models.TextField()
    course_id=models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
    session_year_id=models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)



class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attdance_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)

class AttdanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    attdance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class LeaveReportStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=200)
    leave_message=models.TextField()
    leave_status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class LeaveReportStaff(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=200)
    leave_message=models.TextField()
    leave_status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class FeedbackStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    feedback=models.TextField()
    feedback_reply=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()



class FeedbackStaff(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    feedback=models.TextField()
    feedback_reply=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class NotificationStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class NotificationStaff(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance,created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance,address="")
        if instance.user_type==3:
            Student.objects.create(admin=instance,course_id=Courses.objects.get(id=1),profile_pic="",session_started_at="2022-01-01",session_end_at="2025-01-01")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()  
    if instance.user_type == 3:
        instance.student.save()

    

        
    
