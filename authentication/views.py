from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect


def login_page(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

    context = {
        "form": form,
    }

    return render(request, 'authentication/login.html', context)


def register_page(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')

    context = {
        "form": form,
    }

    return render(request, 'authentication/register.html', context)


def redirect_to_login(request):
    return redirect("login")
