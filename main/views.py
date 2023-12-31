from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import datetime as dt
from .models import VtcHour, TenTenHour
import pandas as pd
from io import BytesIO
from django.utils import timezone


# Create your views here.

def Home(request):

    if request.method == 'POST':

        curr_user = request.user

        curr_user.employee_details.first_login = False

        curr_user.employee_details.save()

        return redirect('/logout/')

    return render(request, 'main/home.html', {})


@login_required(login_url='/login')
def ViewHours(request):

    return render(request, 'main/view-hours.html', {})



@login_required(login_url='/login')
@csrf_protect
def AddHour(request):

    if request.method == 'POST':

        try:
            employee = request.POST.get("employee_name")
            class_type = request.POST.get("class_type")
            student = request.POST.get("student")
            school = request.POST.get("school")
            duration = request.POST.get("duration")
            class_date = request.POST.get("class_date")
            class_start = request.POST.get("class_time")
            wage = request.POST.get("wage")
            
            curr_user = request.user
            
            date = dt.datetime.strptime(f'{class_date} {class_start}:00', '%Y-%m-%d %H:%M:%S')
            print(class_type)

            if "TenTen" in class_type:
                tenDetails = curr_user.employee_details.ten_ten_details

                hour = TenTenHour(ten_ten_details = tenDetails, employee = employee, class_type = class_type, date=date, \
                            duration = duration, submitted = False, wage = wage, school = school)

            else:
                
                vtcDetails = curr_user.employee_details.vtc_details

                if "Private" in class_type:

                    hour = VtcHour(vtc_details = vtcDetails, employee = employee, class_type = class_type, date=date, \
                            duration = duration, submitted = False, wage = wage, student = student)
                else:
                    hour = VtcHour(vtc_details = vtcDetails, employee = employee, class_type = class_type, date=date, \
                            duration = duration, submitted = False, wage = wage)
            
            hour.save()

            return HttpResponse(status = 204)
        
        except Exception as e:
            
            return HttpResponse(status = 500)

    else:
        return render(request,'main/add-hours.html', {})


@login_required(login_url='/login')
def LoadTable(request, load_year, load_month):

    curr_user_details = request.user.employee_details

    start_date = dt.datetime(load_year, load_month, 1)

    end_date = dt.datetime(load_year, load_month + 1, 1) if load_month < 12 else dt.datetime(load_year + 1, 1, 1)
    
    emptyQuery = User.objects.filter(id=0)

    vtcQuery = emptyQuery

    tenQuery = emptyQuery
    
    if curr_user_details.is_vtc_coach:
        
        vtcQuery = curr_user_details.vtc_details.vtchour_set.filter(date__gte=start_date, date__lt=end_date)

        vtcQuery = vtcQuery.order_by('-date')

    if curr_user_details.is_ten_ten_employee:
        
        tenQuery = curr_user_details.ten_ten_details.tentenhour_set.filter(date__gte=start_date, date__lt=end_date)

        tenQuery = tenQuery.order_by('-date')

    var_pass = {
        "TenTenHours":tenQuery,
        "VtcHours":vtcQuery
    }

    return render(request, 'main/two-tables.html', var_pass)

@login_required(login_url='/login')
@csrf_protect
def EditModal(request, dbTable, id):

    curr_user = request.user

    if dbTable == "VTC":
        hour_edit = curr_user.employee_details.vtc_details.vtchour_set.get(id = id)

        field_names = ["Coach",
                       "Lesson Type",
                       "Lesson Date",
                       "Lesson Start Time"]

    elif dbTable == "TenTen":
        hour_edit = curr_user.employee_details.ten_ten_details.tentenhour_set.get(id = id)

        field_names = ["Instructor",
                       "Program Type",
                       "Program Date",
                       "Program Start Time"]

    else:
        raise Exception("No DB Table")

    
    if request.method == "POST":
        
        hour_edit.duration = request.POST.get("duration")

        hour_edit.class_type = request.POST.get("class_type")

        date_str = request.POST.get("class_date")

        start_time = request.POST.get("class_time")

        hour_edit.date = dt.datetime.strptime(f'{date_str} {start_time}:00', '%Y-%m-%d %H:%M:%S')

        if dbTable == 'VTC':

            hour_edit.earning = float(request.POST.get("duration")) * curr_user.employee_details.vtc_details.wage
            
            student = request.POST.get("student")
            
            if hour_edit.class_type == 'VTC Private':
            
                hour_edit.student = student

            else:
                hour_edit.student = ""

        elif dbTable == 'TenTen':

            hour_edit.earning = float(request.POST.get("duration")) * curr_user.employee_details.ten_ten_details.wage
            
            school = request.POST.get("school")

            hour_edit.school = school

        hour_edit.save()

        return HttpResponse(status = 204)
    
    else:

        d = {'hour_to_edit':hour_edit, 
             'hour_type':dbTable,
             'field_names':field_names}

        return render(request, 'main/edit-hours.html', d)


@login_required(login_url='/login')
@csrf_protect
def DeleteHour(request, dbTable, id):

    if request.method == "POST":
        
        curr_user = request.user

        try:

            if dbTable == "TenTen":
                to_delete = curr_user.employee_details.ten_ten_details.tentenhour_set.get(id=id)
            
            elif dbTable == "VTC":
                to_delete = curr_user.employee_details.vtc_details.vtchour_set.get(id=id)

            to_delete.delete()

            return HttpResponse(status = 204)

        except Exception as e:

            return HttpResponse(status = 500)
    else:
        return HttpResponse(status = 400)
    
