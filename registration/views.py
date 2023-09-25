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

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():
            
            form.save()

            user_email = form.cleaned_data['email']

            created_user = User.objects.get(email=user_email)

            # account = Coach(user = curr_user, wage = form.cleaned_data['hourly'])

            # account.save()

            return EmploymentDetailForm(request, created_user)
            
    else:  
        form = RegistrationForm()

        tempPassNum = dt.datetime.now().strftime('%f%S')

        tempPass = f'TenTen{tempPassNum}'
    
    return render(request, 'registration/registration.html', {"form":form, "tempPass":tempPass})


def EmploymentDetailForm(request, created_user):

    if request.method == "POST":
        
        tenEmployee = request.POST.get('TenTen-check') == 'on'
        vtcEmployee = request.POST.get('VTC-check') == 'on'

        employeeDetails = EmploymentDetails(user = created_user, is_ten_ten_employee = tenEmployee, is_vtc_coach = vtcEmployee)

        return redirect

    else:
        return render(request, 'registration/employment-details.html', {})