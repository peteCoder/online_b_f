from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "dashboard/index.html", {})


def main_home(request):
    return render(request, "main/index.html", {})



def login(request):
    return render(request, "dashboard/login.html", {})



def register(request):
    return render(request, "dashboard/register.html", {})





def chartpage(request):
    return render(request, "dashboard/charts-chartjs.html", {})








