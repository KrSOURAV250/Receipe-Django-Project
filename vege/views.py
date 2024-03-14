from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
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
        queryset.receipe_image = receipe_image
        queryset.rdreceipe_description = receipe_description
        if receipe_image:
            queryset.receipe_image = receipe_image
        queryset.save()
        return redirect('/')
    else:
        store = Receipe.objects.get(id=id)
        return render(request, "updateReceipe.html", {'callin': store})


def login(request):
    return render(request, "login.html")


def register_successfully():
    HttpResponse("<h1> Login Successfully </h1>")
    time.sleep(2)


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        User.objects.create(
            first_name=first_name, last_name=last_name, username=username)
        User.set_password(raw_password=password)
        User.save()
        register_successfully()
        redirect('/login')
    return render(request, "register.html")
