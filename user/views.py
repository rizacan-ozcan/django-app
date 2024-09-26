from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .forms import RegisterForm, LoginForm, UserProfileForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        newUser = User(username=username)
        newUser.set_password(password)
        newUser.save()
        login(request, newUser)
        messages.success(request, "Kayıt Başarılı.")
        return redirect("index")
    context = {
        "form": form
    }
    return render(request, "register.html", context)

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Kullanıcı adı veya şifre hatalıdır.")
            return render(request, "login.html", context)
        messages.success(request, "Giriş Başarılı")
        login(request, user)
        next_url = request.POST.get('next') or request.GET.get('next') or '/blog/dashboard'
        return HttpResponseRedirect(next_url)
    return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    messages.success(request, "Basarili bir sekilde cikis yapildi")
    return redirect("index")

@login_required(login_url="user:login")
def profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user:profile", username=user.username)
    else:
        form = UserProfileForm(instance=user)

    context = {
        "form": form,
        "username": user.username
    }
    return render(request, "profile.html", context)