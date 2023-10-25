from django.shortcuts import render
from django.http import HttpResponse

def main_page(request):
    return render(request, 'main/main.html')

def login_page(request):
    return render(request, 'main/login.html')

def home(request):
    return render(request, 'main/home.html')

