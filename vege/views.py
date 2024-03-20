from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from .models import *
import time


# Create your views here.
def receipes(request):
    if request.method == "POST":
        receipe_name = request.POST.get("receipe_name")
        receipe_description = request.POST.get("receipe_description")
        receipe_image = request.FILES.get("receipe_image")
        Receipe.objects.create(
            receipe_name=receipe_name, receipe_description=receipe_description, receipe_image=receipe_image)
        return redirect("/")
    queryset = Receipe.objects.all()
    if request.GET.get("search"):
        queryset = Receipe.objects.filter(
            receipe_name__icontains=request.GET.get("search"))
    elif request.GET.get("search") == '':
        queryset = None
    context = {"receipes": queryset}
    return render(request, "receipes.html", context=context)


def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/')


def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    if request.method == 'POST':
        receipe_name = request.POST.get("receipe_name")
        receipe_description = request.POST.get("receipe_description")
        receipe_image = request.FILES.get("receipe_image")
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        if receipe_image:
            queryset.receipe_image = receipe_image
        queryset.save()
        return redirect('/')
    else:
        store = Receipe.objects.get(id=id)
        return render(request, "updateReceipe.html", {'callin': store})


def login_page(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        if not User.objects.filter(username=user_name).exists():
            messages.error(request, "Username Invalid")
            return redirect('/vege/register')
        user = authenticate(username=user_name, password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect("/vege/login")
        login(request, user=user)
        return redirect("/")
    print(messages)
    return render(request, "login.html", {'messages': messages.get_messages(request)})


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.error(request, "This UserName Already Taken.")
            return redirect("/vege/register")
        a = User.objects.create(
            first_name=first_name, last_name=last_name, username=username)
        a.set_password(raw_password=password)
        a.save()
        messages.success(request, "Regestration Successfully.")
        return redirect('/vege/login')
    return render(request, "register.html")
