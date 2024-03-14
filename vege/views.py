from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *


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
        # print(f"here: -{request.GET.get('search')}-")
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