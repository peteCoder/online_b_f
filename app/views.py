from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "dashboard/index.html", {})


def main_home(request):
    return render(request, "main/index.html", {})



def login(request):
    return render(request, "main/login.html", {})



def register(request):
    return render(request, "main/register.html", {})














