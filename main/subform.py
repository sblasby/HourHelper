from django import forms

class SubmitHourForm(forms.Form):

    startDate = forms.DateField(widget=forms.SelectDateWidget())

    endDate = forms.DateField()

    