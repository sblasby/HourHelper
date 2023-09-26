from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
import datetime as dt
from HourTraker import utils
from .Rform import RegistrationForm
from .models import EmploymentDetails, TenTenEmployee, VTCEmployee

# Create your views here.

@user_passes_test(utils.is_superuser, login_url='/home/')
def Register(request):

    tempPassNum = dt.datetime.now().strftime('%f%S')

    tempPass = f'TenTen{tempPassNum}'

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():
            
            form.save()

            user_name = form.cleaned_data['username']

            created_user = User.objects.get(username=user_name)

            # account = Coach(user = curr_user, wage = form.cleaned_data['hourly'])

            # account.save()

            request.session['createdUsername'] = created_user.username

            return redirect('/employment-details/')
            
    else:  
        form = RegistrationForm()

        request.session['tempPass'] = tempPass
    
        return render(request, 'registration/registration.html', {"form":form, "tempPass":tempPass})


@user_passes_test(utils.is_superuser, login_url='/home/')
def EmploymentDetailForm(request):

    if request.method == "POST":

        created_user = User.objects.get(username = request.session['createdUsername'])

        tempPass = request.session['tempPass']
        
        tenEmployee = request.POST.get('TenTen-check') == 'on'
        vtcEmployee = request.POST.get('VTC-check') == 'on'


        employeeDetails = EmploymentDetails(user = created_user, is_ten_ten_employee = tenEmployee, is_vtc_coach = vtcEmployee)

        employeeDetails.save()

        if tenEmployee:
            wage = request.POST.get('TenTen-wage')
            contracted = request.POST.get('TenTen-payroll') == 'on'
            job_details = TenTenEmployee(details = employeeDetails, wage = wage, is_contract = contracted)
            job_details.save()

        if vtcEmployee:
            wage = request.POST.get('VTC-wage')
            contracted = request.POST.get('VTC-payroll') == 'on'
            job_details = VTCEmployee(details = employeeDetails, wage = wage, is_contract = contracted)
            job_details.save()
        
        return render(request, 'registration/user-success.html', {"firstName":created_user.first_name, "tempPass":tempPass})

    else:
        return render(request, 'registration/employment-details.html', {})
    

