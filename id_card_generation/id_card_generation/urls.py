"""
URL configuration for id_card_generation project.

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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('studenthome/',views.studenthome,name='studenthome'),
    path('facultyhome/', views.facultyhome, name='facultyhome'),
    path('studentdata/', views.studentdata, name='studentdata'),
    path('verify-student/<str:admission_no>/', views.verify_student, name='verify_student'),
    path('pendingupdates/', views.pendingupdates, name='pendingupdates'),
    path('studentform/', views.studentform, name='studentform'),
    path('studentprofile/', views.studentprofile, name='studentprofile'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('adminbase/', views.adminbase, name='adminbase'),
    path('view_verified_students/', views.view_verified_students, name='view_verified_students'),
    path('batch/', views.batch, name='batch'),
    path('department/', views.department, name='department'),
    path('verify_faculty/<int:faculty_id>/', views.verify_faculty, name='verify_faculty'),
    path('facultyverify/', views.facultyverify, name='facultyverify'),
    path('generateid/', views.generateid, name='generateid'),
    path('submit-correction/', views.submit_correction, name='submit_correction'),
    path('updates/', views.view_corrections, name='view_corrections'),
    path('idcard/<str:student_id>/', views.idcard, name='idcard'),
    path('generate_multiple_idcards/', views.generate_multiple_idcards, name='generate_multiple_idcards'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)