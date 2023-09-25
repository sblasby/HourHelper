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

            curr_user = User.objects.get(email=user_email)

            # account = Coach(user = curr_user, wage = form.cleaned_data['hourly'])

            # account.save()

            return render(request, "registration/employment-details.html", {})
            
    else:  
        form = RegistrationForm()

        tempPassNum = dt.datetime.now().strftime('%f%S')

        tempPass = f'TenTen{tempPassNum}'
    
    return render(request, 'registration/registration.html', {"form":form, "tempPass":tempPass})


def EmploymentDetailForm(request):
    return render(request, 'registration/employment-details.html', {})