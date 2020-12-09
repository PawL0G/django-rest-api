from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def login_page(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_page = request.GET.get('next', None)

            if next_page:
                return redirect(next_page)
            else:
                return redirect("dashboard")

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


def logout_page(request):
    logout(request)
    return redirect('login')

