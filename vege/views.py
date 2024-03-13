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
    context = {"receipes": queryset}
    return render(request, "receipes.html", context=context)


def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/')


def update_receipe(request, id):
    if request.method == 'POST':
        Receipe.objects.get(id=id)
        receipe_name = request.POST.get("receipe_name")
        receipe_description = request.POST.get("receipe_description")
        receipe_image = request.FILES.get("receipe_image")
        Receipe(id=id, receipe_name=receipe_name,
                receipe_description=receipe_description, receipe_image=receipe_image).save()
        queryset = Receipe.objects.all()
        context = {"receipes": queryset}
        return redirect('/')
    else:
        store = Receipe.objects.get(id=id)
        return render(request, "updateReceipe.html", {'callin': store})
