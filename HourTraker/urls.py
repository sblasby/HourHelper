"""HourTraker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from main import views as mview
from registration import views as rview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', rview.Register, name="registration"),
    path('home/', mview.Home, name='home'),
    path('', include("django.contrib.auth.urls")),
    path('view-hours/', mview.ViewHours, name="view_hours"),
    path('update-table-<int:load_year>-<int:load_month>/', mview.LoadTable, name="load_table"),
    path('add-hours/', mview.AddHour, name="add_hours"),
    path('register/wrong-key/', rview.WrongKey ,name="wrong_key"),
    path('delete-<int:id>/', mview.DeleteHour, name='delete_hour'),
    path('edit-hour-<int:id>/', mview.EditModal, name = 'edit_hours'),
    path('submit-hours/', mview.SubmitHours, name="submission_page")
]
