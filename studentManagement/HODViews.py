import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from studentManagement.forms import AddStudentForm
from studentManagement.models import Courses, CustomUser, SessionYearModel, Staffs, Student, Subjects
from django.core.files.storage import FileSystemStorage
from .forms import AddStudentForm



def session_year(request):
    return render(request,'HOD_template/manage_session.html')


def add_session_save(request):
    if request.method!="POST":
        return HttpResponse('<h2>Method is not allowed</h2>', status=405)
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")
        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session added successfully.")
            return redirect('/add_session')  # or whatever URL you want
        except Exception as e:
            messages.error(request, f'Faild to add Session Year:{str(e)}')
            return HttpResponseRedirect(reverse('session_year'))

def admin_home(request):
    # Fetch users based on user_type
    admin = CustomUser.objects.filter(user_type='1')  # HOD
    staff = CustomUser.objects.filter(user_type='2')  # Staff
    student = CustomUser.objects.filter(user_type='3')  # Student

    # Pass the data to the template
    return render(request, 'HOD_template/home_content.html', {
        'admin': admin,
        'staff': staff,
        'student': student,
    })


def add_staff(request):
    return render(request, "HOD_template/add_staff.html" )

def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("lname")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect("/add_staff")
        except Exception as e:
             messages.error(request, f"Failed to Add Staff: {str(e)}")
        return HttpResponseRedirect("/add_staff")


def add_course(request):
    return render(request,"HOD_template/add_course.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Can not add course")
    else:
        course=request.POST.get("course")

    if not course:
        messages.error(request, "Course name is required.")
        return HttpResponseRedirect("/add_course")
    
    try:
        course_model=Courses(course_name=course)
        course_model.save()
        messages.success(request,"Successfully added course")
    except Exception as e:
        messages.error(request,f"Faild to add course: {str(e)}")
    return HttpResponseRedirect("/add_course")
    



def add_student(request):
    courses=Courses.objects.all()
    form=AddStudentForm()
    context={
        'courses':courses,
        'form':form
    }
    return render(request,"HOD_template/add_student.html",context)


def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Cannot Add Student Currently!.")
    else:
        form=AddStudentForm(request.POST, request.FILES) 
        if form.is_valid():
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["lname"]
            username=form.cleaned_data["username"]
            address=form.cleaned_data["address"]
            course_id=form.cleaned_data["course"]
            sex=form.cleaned_data["sex"]
            session_start=form.cleaned_data["Session_start"]
            session_end=form.cleaned_data["Session_end"]
            profile=request.FILES.get("profile")
            fs=FileSystemStorage()
            filename=fs.save(profile.name,profile)
            profile_url=fs.url(filename )

            if not course_id:
                messages.error(request, "Course is required")
                return HttpResponseRedirect("/add_student")
            try:
                user=CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    user_type=3,
                    )
                student = user.student # ✅ this works because OneToOneField creates a reverse relation
                student.address = address
                student.course_id = Courses.objects.get(id=course_id)
                student.session_started_at = session_start
                student.session_end_at = session_end
                student.gender = sex
                student.profile_pic = profile_url  # Or handle upload
                student.save()
                # user.students.address=address
                # course_obj=Courses.objects.get(id=course_id)
                # # user.students.course_id=course_obj

                # start_date=datetime.datetime.strptime(session_start, '%d-%m-%y').date()
                # end_date=datetime.datetime.strptime(session_end, '%d-%m-%y').date()


                # Student.objects.create(
                #     admin=user, address=address,course_id=course_obj,session_started_at=start_date,session_end_at=end_date,gender=sex,profile_pic="",
                # )
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect("/add_student")
            except Exception as e:
                messages.error(request,f"Faild to add student: {str(e)}")
            return HttpResponseRedirect("/add_student")
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, "HOD_template/add_student.html", {"form": form})


        

def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    context={
        'courses':courses,
        'staffs':staffs

    }
    return render(request,"HOD_template/add_subject.html",context)


def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Can not save subject")
    else:
        subject_name=request.POST.get("subject")
        course_id=request.POST.get("course")
        course_name=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff_name=CustomUser.objects.get(id=staff_id)

        try:
            subject=Subjects.objects.create(
                 subject_name=subject_name,
                 course_id=course_name,
                 staff_id=staff_name
            )
            subject.save()
            messages.success(request,"Successfully added subject")
            return HttpResponseRedirect("/add_subject")
        except Exception as e:
            messages.error(request,f"Faild to add subject {str(e)}:")
        return HttpResponseRedirect("/add_subject")



def manage_staff(request):
    staffs=Staffs.objects.all()
    context={
        "staffs":staffs
    }
    return render(request, "HOD_template/manage_staff.html",context)


def edit_staff(request,staff_id):
    staff = get_object_or_404(Staffs, admin_id=staff_id)
    context={
        "staff":staff,
        "id":staff_id
    }
    return render(request, "HOD_template/edit_staff.html",context)

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("lname")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address") 
        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin_id=staff_id)   
            staff_model.address=address
            staff_model.save()

            messages.success(request, "Successfully Edited Staff")
            return HttpResponseRedirect(f"/edit_staff/{staff_id}/")
        except Exception as e:
            messages.error(request, f"Failed to edit staff: {str(e)}")
            return HttpResponseRedirect(f"/edit_staff/{staff_id}/")
   
            

def manage_student(request):
    students=Student.objects.all()
    context={
        "students":students
    }
    return render(request, "HOD_template/manage_student.html",context)

def edit_student(request,student_id):
    student=get_object_or_404(Student, admin=student_id)
    courses=Courses.objects.all()
    context={
        "student":student,
        "courses":courses,
        "id":student_id
    }
    return render(request,"HOD_template/edit_student.html",context)

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse(request,"<h2>Method is not allowed</h2>")
    else:
        student_id=request.POST.get("student_id")
        email=request.POST.get("email")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("lname")
        username=request.POST.get("username")
        address=request.POST.get("address")
        session_start=request.POST.get("Session_start")
        session_end=request.POST.get("Session_end")
        course_id=request.POST.get("course")
        sex=request.POST.get("sex")

        if request.FILES.get('profile', False):
            profile=request.FILES['profile']
            fs=FileSystemStorage()
            filename=fs.save(profile.name,profile)
            profile_url=fs.url(filename)
        else:
            profile_url=None


        try:
            
            user=CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.email=email
            user.username=username
            user.last_name=last_name
            user.save()

            student_model=Student.objects.get(admin_id=student_id)
            student_model.address=address
            student_model.session_start=session_start
            student_model.session_end=session_end
            student_model.sex=sex
            student_model.save()

            course=Courses.objects.get(id=course_id)
            student_model.course_id=course
            if profile_url!=None:
                student_model.profile=profile_url
            student_model.save()

            messages.success(request, "Successfully Edited student")
            return HttpResponseRedirect("/edit_student/{student_id}/")
        except Exception as e:
            messages.error(request, f"Failed to edit student: {str(e)}")
            return HttpResponseRedirect(f"/edit_student/{student_id}/")


def manage_course(request):
    courses=Courses.objects.all()
    context={
        "courses":courses
    }
    return render(request,"HOD_template/manage_course.html",context)

def edit_course(request,course_id):
    course=get_object_or_404(Courses,id=course_id)
    context={
        "course":course,
        "id":course_id
    }
    return render(request,"HOD_template/edit_course.html",context)

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method is not alloweed</h2>")
    else:
        course_id=request.POST.get('course_id')
        course_name=request.POST.get("course")
        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            messages.success(request, "Successfully Edited Courses")
            return HttpResponseRedirect(f"/edit_course/{course_id}/")
        except Exception as e:
            messages.error(request, f"Failed to edit Courses: {str(e)}")
            return HttpResponseRedirect(f"/edit_course/{course_id}/")



def manage_subject(request):
    subjects=Subjects.objects.all()
    context={
        "subjects":subjects
    }
    return render(request, "HOD_template/manage_subject.html",context)

def edit_subject(request,subject_id):
    subject=get_object_or_404(Subjects, id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    context={
        "subject":subject,
        "courses":courses,
        "staffs":staffs,
        "id":subject_id
    }
    return render(request, "HOD_template/edit_subject.html",context)

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject")
        course_id=request.POST.get("course")
        staff_id=request.POST.get("staff")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            subject.course_id=Courses.objects.get(id=course_id)
            subject.staff_id=CustomUser.objects.get(id=staff_id)
            subject.save()
            
            messages.success(request, "Subject updated successfully.")
            return HttpResponseRedirect(f"/edit_subject/{subject_id}/")
        except Exception as e:
            messages.error(request, f"Error updating subject: {e}")
            return HttpResponseRedirect(reverse("edit_subject", subject_id))

