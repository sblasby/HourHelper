from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .Rform import RegistrationForm
from .models import Coach

# Create your views here.

def Register(request):

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():
            
            if form.cleaned_data['reg_key'] == 'TenTen':

                form.save()

                user_email = form.cleaned_data['email']

                curr_user = User.objects.get(email=user_email)

                account = Coach(user = curr_user, wage = form.cleaned_data['hourly'])

                account.save()

                return redirect("/login")
            
            else:
                return redirect("/register/wrong-key")
    
    else:  
        form = RegistrationForm()
    
    return render(request, 'registration/registration.html', {"form":form})

def WrongKey(request):

    form = RegistrationForm()
    
    return render(request, "registration/wrong-key.html", {"form":form})