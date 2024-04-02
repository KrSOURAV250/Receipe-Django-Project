from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q, Sum
from .models import *


# Create your views here.
@login_required(login_url="/vege/loginn")
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
        queryset = Receipe.objects.filter(Q(receipe_name__icontains=request.GET.get(
            "search")) | Q(receipe_description__icontains=request.GET.get("search")))
    elif request.GET.get("search") == '':
        queryset = None
    context = {"receipes": queryset}
    return render(request, "receipes.html", context=context)


@login_required(login_url="/vege/loginn")
def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    sub = "Recipe Deleted"
    message_text = f"""Hey {request.user.first_name}, Your Recipe Have Been Deleted Successfully."""
    sender = "theappishere@gmail.com"
    reciver = [request.user.email]
    send_mail(subject=sub, message=message_text,
              from_email=sender, recipient_list=reciver, fail_silently=False)
    return redirect('/')


@login_required(login_url="/vege/loginn")
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
        sub = "Recipe Updated"
        message_text = f"""Hey {request.user.first_name}, Your Recipe Have Been Updated Successfully."""
        sender = "theappishere@gmail.com"
        reciver = [request.user.email]
        send_mail(subject=sub, message=message_text,
                  from_email=sender, recipient_list=reciver, fail_silently=False)
        return redirect('/')
    else:
        store = Receipe.objects.get(id=id)
        return render(request, "updateReceipe.html", {'callin': store})


def login_page(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        if not User.objects.filter(username=user_name).exists():
            messages.error(request, message="Invalid Username.")
            return redirect(to="/vege/loginn")
        user = authenticate(username=user_name, password=password)
        if user:
            login(request, user=user)
            messages.success(request, message="Login Successfully.")
            sub = "Logged In"
            message_text = f"""Hey {request.user.first_name}, You Have Been Logged In Successfully."""
            sender = "theappishere@gmail.com"
            reciver = [request.user.email]
            send_mail(subject=sub, message=message_text,
                      from_email=sender, recipient_list=reciver, fail_silently=False)
            return redirect(to='/')
        messages.error(request, message="Invalid Password.")
        return redirect(to="/vege/loginn")
    return render(request, "login.html")


@login_required(login_url="/vege/loginn")
def logout_page(request):
    first_name = request.user.first_name
    email = request.user.email
    logout(request)
    messages.info(request, message="Logged Out.")
    sub = "Logged Out"
    message_text = f"""Hey {first_name}, You Have Been Logged Out Successfully."""
    sender = "theappishere@gmail.com"
    reciver = [email]
    send_mail(subject=sub, message=message_text,
              from_email=sender, recipient_list=reciver, fail_silently=False)
    return redirect("/vege/loginn")


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("user_email")
        password = request.POST.get("user_password")
        if User.objects.filter(username=username).exists():
            messages.error(request, "This UserName Already Taken.")
            return redirect("register")
        else:
            a = User.objects.create(
                first_name=first_name, last_name=last_name, username=username, email=email)
            a.set_password(raw_password=password)
            a.save()
            messages.success(request, "Regestration Successfully.")
            sub = "Welcome To This APP"
            message_text = f"""Hey {first_name}, You Have Registered Successfully."""
            sender = "theappishere@gmail.com"
            reciver = [email]
            send_mail(subject=sub, message=message_text,
                      from_email=sender, recipient_list=reciver, fail_silently=False)
            return redirect('login')
    return render(request, "register.html")


@login_required(login_url="/vege/loginn")
def get_students(request):
    queryset = Student.objects.all()
    search = request.GET.get("search")
    if search:
        queryset = queryset.filter(Q(student_name__icontains=search) | Q(student_id__student_id__icontains=search) | Q(
            student_email__icontains=search) | Q(student_age__icontains=search) | Q(student_address__icontains=search) | Q(department__department__icontains=search))
    paginator = Paginator(queryset, 7)
    page_no = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_no)
    return render(request, template_name="report/students.html", context={"queryset": page_obj})


def see_marks(request, student_id):
    queryset = SubjectMarks.objects.filter(
        student__student_id__student_id=student_id)
    total_marks = queryset.aaggregate(total_marks=Sum("marks"))
    return render(request, template_name="seeMarks.html", context={"qs": queryset, "total_marks": total_marks})
