from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from django.shortcuts import render


from . import forms


def logout_user(request):
    """Simple log out django defaut function

    Args:
        request (GET): User model_

    Returns:
        redirect: login page
    """
    logout(request)
    return redirect('login')


def login_page(request):
    """This function allows user to log himself 
    by filling the form

    Args:
        request (POST): Login form for user model

    Returns:
        render: main home page
    """
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
    """This function allows new user to creat account

    Args:
        request (POST): User model

    Returns:
        render : login page
    """
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        try:
            if form.is_valid:
                form.save()
                login_page(request)
            return redirect('home')
        except ValueError:
            return render(request, 'authenticate/signup.html', context={'form': form})
    return render(request, 'authenticate/signup.html', context={'form': form})
