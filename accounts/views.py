from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts.forms import SignupForm, LoginForm


def signup(request, *args, **kwargs):
    user = request.user

    if user.is_authenticated:
        return redirect('home')
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = request.session["email"] = form.cleaned_data["email"].lower()
            password = request.session["email"] = form.cleaned_data["password1"]
            user = authenticate(email=email, password=password)
            login(request, user)

            if destination := kwargs.get("next"):
                """
                if destination := kwargs.get("next"): equivalent à 
                ( destination = kwargs.get("next")
            if destination :
                return redirect(destination))
                """
                return redirect(destination)
            else:
                return redirect('home')
        else:
            messages.error(request, form.errors)
    context = {"form": form}
    return render(request, 'accounts/signup.html', context)


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.session['email'] = form.cleaned_data['email']
            password = form.cleaned_data["password"]
            if user := authenticate(request, email=email, password=password):
                login(request, user)
                return redirect('home')
        else:
            messages.info(request, form.non_field_errors())
    context = {"form": form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')
