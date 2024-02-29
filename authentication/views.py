from django.shortcuts import render, redirect
from .forms import UserCreationForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import auth
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('/main/scrape')
    return render(request, 'authentication/home.html')
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                auth.login(request, user)
                return redirect('/main/scrape')
    return render(request, 'authentication/login.html', {'form': form})

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'authentication/register.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('home')