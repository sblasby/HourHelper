from django.shortcuts import render

# Create your views here.


def MasterTable(request):
    return render(request, "master/master-table.html", {})