from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import datetime as dt
from main.models import VtcHour, TenTenHour
import pandas as pd
from io import BytesIO


@login_required(login_url='/login')
def CreateSheet(request):

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

        return render(request, 'submissions/submit-hours.html', {})
        

