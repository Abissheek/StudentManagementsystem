from django import forms
from django.forms.widgets import TextInput,EmailInput,Select, FileInput,DateInput
from studentManagement.models import Courses

# class DateInput(forms.DateInput):
#     input_type="date"

class AddStudentForm(forms.Form):
    email=forms.EmailField(
        label="Email",
        max_length=50, 
        widget=EmailInput(attrs={
            'class':'form-control', 
            'placeholder':'enter email'
            }))
    password=forms.CharField(
        label="Password",max_length=50,
        widget=forms.PasswordInput(attrs={
            'class':'form-control', 'placeholder':'enter password'
        }))
    first_name=forms.CharField(
        label="First Name",
        max_length=50,
        widget=TextInput(attrs={
            'class':'form-control',
            'placeholder':' Enter First Name'
        }))
    lname=forms.CharField(label="Last Name",max_length=50, widget=TextInput(attrs={
            'class':'form-control',
            'placeholder':' Enter Last Name'
        }))
    username=forms.CharField(label="Username",max_length=50, widget=TextInput(attrs={
            'class':'form-control',
            'placeholder':' Enter Username'
        }))
    address=forms.CharField(label="Address",max_length=50, widget=TextInput(attrs={
            'class':'form-control',
            'placeholder':' Enter Address'
        }))
    
    courses=Courses.objects.all()
    course_list=[]
    try:
        for course in courses:
            small_course=(course.id,course.course_name)
            course_list.append(small_course)
    except:
        course_list=[]

    course=forms.ChoiceField(label="Course",choices=course_list, widget=Select(attrs={
            'class':'form-control',
        }))

    gender_choice=(
       ("Male","Male"),
       ( "Female","Female")
    )
    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=Select(attrs={
            'class':'form-control',
        }))
    Session_start=forms.DateField(label="Session Start", widget=DateInput(attrs={'type':'date', 'class':'form-control'}))
    Session_end=forms.DateField(label="Session End", widget=DateInput(attrs={'type':'date','class':'form-control'}) )
    profile=forms.FileField(label="Profile",max_length=50, required=False, widget=FileInput(attrs={'class':'form-control'})) 

   



class EditStudentForm(forms.Form):
    email=forms.EmailField(
        label="Email",
        max_length=50, 
        widget=EmailInput(attrs={
            'class':'form-control', 
            'placeholder':'enter email'
            }))
    first_name=forms.CharField(
        label="First Name",
        max_length=50,
        widget=TextInput(attrs={
            'class':'form-control',
            'placeholder':' Enter First Name'
        }))
    lname=forms.CharField(label="Last Name",max_length=50, widget=TextInput(attrs={
            'class':'form-control',
            'placeholder':' Enter Last Name'
        }))
    username=forms.CharField(label="Username",max_length=50, widget=TextInput(attrs={
            'class':'form-control',
            'placeholder':' Enter Username'
        }))
    address=forms.CharField(label="Address",max_length=50, widget=TextInput(attrs={
            'class':'form-control',
            'placeholder':' Enter Address'
        }))

    courses=Courses.objects.all()
    course_list=[]
    try:

        for course in courses:
            small_course=(course.id,course.course_name)
            course_list.append(small_course)
    except:
        course_list=[]

    course=forms.ChoiceField(label="Course",choices=course_list, widget=Select(attrs={
            'class':'form-control',
        }))

    gender_choice=(
       ("Male","Male"),
       ( "Female","Female")
    )
    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=Select(attrs={
            'class':'form-control',
        }))
    Session_start=forms.DateField(label="Session Start", widget=DateInput(attrs={'type':'date', 'class':'form-control'}))
    Session_end=forms.DateField(label="Session End", widget=DateInput(attrs={'type':'date','class':'form-control'}) )
    profile=forms.FileField(label="Profile",max_length=50, required=False, widget=FileInput(attrs={'class':'form-control'})) 

   
