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
from submissions import views as sview
from master import views as masview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', rview.Register, name="registration"),
    path('home/', mview.Home, name='home'),
    path('', include("django.contrib.auth.urls")),
    path('view-hours/', mview.ViewHours, name="view_hours"),
    path('update-tables-<int:load_year>-<int:load_month>/', mview.LoadTable, name="load_table"),
    path('add-hours/', mview.AddHour, name="add_hours"),
    path('delete-<str:dbTable>-<int:id>/', mview.DeleteHour, name='delete_hour'),
    path('edit-hour-<str:dbTable>-<int:id>/', mview.EditModal, name = 'edit_hours'),
    path('create-sheet/', sview.CreateSheet, name="create_sheet"),
    path('employment-details/', rview.EmploymentDetailForm, name="employee_details"),
    path('', mview.Home, name='home_empty'),
    path('master-table/', masview.MasterTable, name='Master Table'),
]
