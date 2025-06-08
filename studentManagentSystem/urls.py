"""
URL configuration for studentManagentSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from  studentManagement import HODViews, staffViews, studentViews, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/',views.showDemoPage),
    path('',views.showLoginPage,name='show_login'),
    path('log_out_user',views.LogOutUser,name="log_out_user"),
    path('doLogin',views.doLogin,name='doLogin'),
    path('admin_home',HODViews.admin_home,name='admin_home'),
    path('add_staff_save',HODViews.add_staff_save, name="add_staff_save"),
    path('add_staff',HODViews.add_staff,name="add_staff"),
    path('add_course',HODViews.add_course, name="add_course"),
    path('add_course_save',HODViews.add_course_save, name=""),
    path('add_student',HODViews.add_student, name="add_student"),
    path('add_student_save',HODViews.add_student_save, name="add_student_save"),
    path('add_subject',HODViews.add_subject,name='add_subject'),
    path('add_subject_save',HODViews.add_subject_save,name='add_subject_save'),
    path('manage_staff',HODViews.manage_staff,name='manage_staff'),
    path('edit_staff/<int:staff_id>/',HODViews.edit_staff,name='edit_staff'),
    path('edit_staff_save/',HODViews.edit_staff_save,name='edit_staff_save'),
    path('manage_student',HODViews.manage_student,name='manage_student'),
    path('edit_student/<int:student_id>/',HODViews.edit_student,name='edit_student'),
    path('edit_student_save/',HODViews.edit_student_save,name='edit_student_save'),
    path('manage_course',HODViews.manage_course,name='manage_course'),
    path('edit_course/<int:course_id>/',HODViews.edit_course,name='edit_course'),
    path('manage_subject',HODViews.manage_subject,name='manage_subject'),
    path('edit_subject/<str:subject_id>/',HODViews.edit_subject,name='edit_subject'),
    path('edit_subject_save',HODViews.edit_subject_save,name='edit_subject_save'),
    path('edit_course_save',HODViews.edit_course_save,name="edit_course_save"),
    path('session_year',HODViews.session_year,name="session_year"),
    path('add_session_save',HODViews.add_session_save,name="add_session_save"),


    #staff Urls,

    path('staff_home',staffViews.staff_home,name='staff_home'),


    #student Urls,
    path('student_home', studentViews.student_home,name='student_home'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) \
+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
