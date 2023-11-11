from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import datetime as dt
from main.models import VtcHour, TenTenHour
import pandas as pd
from io import BytesIO
from collections import namedtuple


@login_required(login_url='/login')
def CreateSheet(request):

    if request.method == "POST":
        
        curr_user = request.user

        curr_details = curr_user.employee_details

        table_type = request.POST.get('which_table')

        start_date = dt.datetime.strptime(request.POST.get('start-date'), '%Y-%m-%d')

        end_date = dt.datetime.strptime(request.POST.get('end-date'), '%Y-%m-%d')

        submission_year_month = dt.datetime.strftime(end_date, '%Y-%m')

        month_name = end_date.strftime('%B')
        
        end_date = end_date + dt.timedelta(days=1)

        query_set = []

        hourly = []

        Wage = namedtuple("Wage", ["wage", "employment"])

        if table_type == "VTC" or table_type == "Both":
            
            vtcSet = curr_details.vtc_details.vtchour_set.filter(date__range=(start_date, end_date))
            
            query_set.extend(list(vtcSet))
            
            hourly.append(Wage(curr_details.vtc_details.wage, "VTC"))
        
        if table_type == "TenTen" or table_type == "Both":
            
            tenSet = curr_details.ten_ten_details.tentenhour_set.filter(date__range=(start_date, end_date))
            
            query_set.extend(list(tenSet))

            hourly.append(Wage(curr_details.ten_ten_details.wage, "TenTen"))

        dataFrame = _createDataFrame(query_set, hourly, month_name)
        
        output = BytesIO()

        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        dataFrame.to_excel(writer, sheet_name='Sheet1', index=False)

        worksheet = writer.sheets['Sheet1']

        worksheet.autofit()
        
        writer.close()  # Close the writer

        output.seek(0)

        # Create a response and set appropriate headers for downloading
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={curr_user.first_name}_{curr_user.last_name}_{submission_year_month}_Hours.xlsx'

        return response

    else:

        return render(request, 'submissions/download-sheet.html', {})
        

def _createDataFrame(query_set, hourly, month_name):

    class_set = sorted(query_set, key = lambda item: item.date)

    dataDict = {f'{month_name} Hours': [],
                    "Date":[],
                    "Start Time":[],
                    "Lesson Type":[],
                    "Duration (hr)":[],
                    "Earnings (CDN)":[]}


    totalHours = 0

    totalEarn = 0

    ind = 0

    for work in class_set:
        
        dataDict["Date"].append(work.date.strftime('%m-%d'))

        dataDict["Start Time"].append(work.date.strftime('%I:%M %p'))

        if work.class_type == 'VTC Private':
            dataDict['Lesson Type'].append(work.class_type + ' - ' + work.student)
        
        elif work.class_type == "TenTen After School":
            dataDict['Lesson Type'].append(work.class_type + ' - ' + work.school)
        
        else:
            dataDict['Lesson Type'].append(work.class_type)

        dataDict["Duration (hr)"].append(work.duration)

        dataDict["Earnings (CDN)"].append(work.earning)

        totalHours += work.duration

        totalEarn += work.earning

        if ind == 0:
            dataDict[f'{month_name} Hours'].append(f'Hourly (CDN)')

        elif ind < len(hourly) + 1:
            
            wage = hourly[ind - 1].wage
            
            name = hourly[ind - 1].employment
            
            dataDict[f'{month_name} Hours'].append(f'{name}: ${wage}')

        else:
            dataDict[f'{month_name} Hours'].append('')
        
        ind += 1

    dataFrame = pd.DataFrame(data=dataDict)

    ## Add the total row
    totalRow = {f'{month_name} Hours': ['', 'Total:'],
                    "Date":['',''],
                    "Start Time":['',''],
                    "Lesson Type":['',''],
                    "Duration (hr)":['', totalHours],
                    "Earnings (CDN)":['', totalEarn]}

    dataFrame = pd.concat([dataFrame, pd.DataFrame(totalRow)], ignore_index=True)

    return dataFrame

