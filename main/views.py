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
            employee = request.POST.get("coach_name")
            class_type = request.POST.get("lesson_type")
            student = request.POST.get("student")
            school = request.POST.get("school")
            duration = request.POST.get("duration")
            class_date = request.POST.get("lesson_date")
            class_start = request.POST.get("lesson_time")
            wage = request.POST.get("wage")
            curr_user = request.user
            
            date = dt.datetime.strptime(f'{class_date} {class_start}:00', '%Y-%m-%d %H:%M:%S')

            if class_type == "VTC Private":

                ls = Lesson(user = curr_user, coach = coach, lesson_type = lesson_type, date=date, \
                        duration = duration, submitted = False, wage = wage, student = student)
            else:
                ls = Lesson(user= curr_user, coach = coach, lesson_type = lesson_type, date=date, \
                        duration = duration, submitted = False, wage = wage)

            ls.save()

            return HttpResponse(status = 204)
        
        except Exception as e:
            
            return HttpResponse(status = 500)

    else:
        return render(request,'main/add-hours.html', {})


@login_required(login_url='/login')
def LoadTable(request, load_year, load_month):

    curr_user = request.user

    start_date = dt.datetime(load_year, load_month, 1)

    end_date = dt.datetime(load_year, load_month + 1, 1) if load_month < 12 else dt.datetime(load_year + 1, 1, 1)
    
    lessons = curr_user.lesson_set.filter(date__gte=start_date, date__lt=end_date)

    lessons = lessons.order_by('-date')

    var_pass = {
        "lessons":lessons
    }

    return render(request, 'main/table-entries.html', var_pass)

@login_required(login_url='/login')
@csrf_protect
def EditModal(request, id):

    curr_user = request.user

    lesson_edit = curr_user.lesson_set.get(id=id)

    if request.method == "POST":
        
        lesson_edit.duration = request.POST.get("duration")

        lesson_edit.lesson_type = request.POST.get("lesson_type")

        date_str = request.POST.get("lesson_date")

        start_time = request.POST.get("lesson_time")

        lesson_edit.date = dt.datetime.strptime(f'{date_str} {start_time}:00', '%Y-%m-%d %H:%M:%S')

        lesson_edit.earning = float(request.POST.get("duration")) * curr_user.account_info.wage

        student = request.POST.get("student")

        if student and lesson_edit.lesson_type == 'VTC Private':
            
            lesson_edit.student = student

        else:
            lesson_edit.student = ""

        lesson_edit.save()

        return HttpResponse(status = 204)
    
    else:

        return render(request, 'main/edit-hours.html', {'lesson_to_edit':lesson_edit})


@login_required(login_url='/login')
@csrf_protect
def DeleteHour(request, id):

    if request.method == "POST":
        
        curr_user = request.user

        try:
            to_delete = curr_user.lesson_set.get(id=id)

            to_delete.delete()

            return HttpResponse(status = 204)

        except Exception as e:

            return HttpResponse(status = 500)
    else:
        return HttpResponse(status = 400)
    
    
@login_required(login_url='/login')
def SubmitHours(request):

    if request.method == "POST":
        
        curr_user = request.user
        
        submission_month = request.POST.get('submission-month')

        submission_month_datetime = dt.datetime.strptime(submission_month, '%Y-%m')

        month_name = submission_month_datetime.strftime('%B')

        hourly = curr_user.account_info.wage

        start_date = dt.datetime.strptime(request.POST.get('start-date'), '%Y-%m-%d')

        end_date = dt.datetime.strptime(request.POST.get('end-date'), '%Y-%m-%d')

        end_date = end_date + dt.timedelta(days=1)

        lesson_set = curr_user.lesson_set.filter(date__range=(start_date, end_date))

        lesson_set = lesson_set.order_by('date')

        dataDict = {f'{month_name} Hours': [],
                        "Date":[],
                        "Start Time":[],
                        "Lesson Type":[],
                        "Duration (hr)":[],
                        "Earnings (CDN)":[]}

        addEmptyStr = False

        totalHours = 0

        totalEarn = 0

        for lesson in lesson_set:
            
            dataDict["Date"].append(lesson.date.strftime('%m-%d'))

            dataDict["Start Time"].append(lesson.date.strftime('%I:%M %p'))

            if lesson.lesson_type == 'VTC Private':
                dataDict['Lesson Type'].append(lesson.lesson_type + ' - ' + lesson.student)
            else:
                dataDict['Lesson Type'].append(lesson.lesson_type)

            dataDict["Duration (hr)"].append(lesson.duration)

            dataDict["Earnings (CDN)"].append(lesson.earning)

            totalHours += lesson.duration

            totalEarn += lesson.earning


            if addEmptyStr:
                dataDict[f'{month_name} Hours'].append('')

            else:
                dataDict[f'{month_name} Hours'].append(f'Hourly (CDN): {hourly}')
                addEmptyStr = True

            lesson.submitted = True

            lesson.save()

        ## Add the total row
        totalRow = {f'{month_name} Hours': ['', 'Total:'],
                        "Date":['',''],
                        "Start Time":['',''],
                        "Lesson Type":['',''],
                        "Duration (hr)":['', totalHours],
                        "Earnings (CDN)":['', totalEarn]}

        

        dataFrame = pd.DataFrame(data=dataDict)

        dataFrame = pd.concat([dataFrame, pd.DataFrame(totalRow)], ignore_index=True)
        
        output = BytesIO()

        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        dataFrame.to_excel(writer, sheet_name='Sheet1', index=False)

        worksheet = writer.sheets['Sheet1']

        worksheet.autofit()
        
        writer.close()  # Close the writer

        output.seek(0)

        # Create a response and set appropriate headers for downloading
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={curr_user.first_name}_{curr_user.last_name}_{submission_month}_Hours.xlsx'

        return response

    else:

        return render(request, 'main/submit-hours.html', {})
        
