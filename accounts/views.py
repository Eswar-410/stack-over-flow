from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('accounts:login')

    else:
        return render(request, 'login.html')


def signup_page(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('accounts:login')

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


def logout_user(request):

    logout(request)

    return redirect('home')
