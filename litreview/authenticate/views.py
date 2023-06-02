from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from django.shortcuts import render


from django.conf import settings
from . import forms


def logout_user(request):
    logout(request)
    return redirect('login')


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'authenticate/login.html', context={'form': form, 'message': message})


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid:
            user = form.save()
            login_page(request, user)
        return redirect('home')
    return render(request, 'authenticate/signup.html', context={'form': form})
