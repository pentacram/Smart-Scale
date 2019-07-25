from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
import datetime
from .forms import *
from  .models import *
from datetime import date

from django.views.generic.dates import MonthArchiveView




now = datetime.datetime.now()
current_date = now.strftime("%Y-%m-%d").split("-")[::-1]
current_date = [int(x) for x in current_date]

# Create your views here.

context = {}


def LoginView(request):
    context['login_form'] = LoginForm()
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect('home')
                else:
                    messages.error(request, "İstifadəçi adı və ya Şifrə yanlışdır!")
                    return redirect("/login")

            else:
                return redirect('/login')
        return render(request, 'login.html', context)
    else:
        return redirect('home')


def LogOutView(request):
    logout(request)
    return redirect('/login')


@login_required(login_url=reverse_lazy('login'))
def HomeView(request):
    object = InfoFields.objects.filter(username__pk=request.user.pk)
    form = RegisterForm()
    context['object'] = object
    if request.method == "POST":
        form = RegisterForm(request.POST)
        form.instance.username = request.user
        born_date = request.POST.get('age').split("/")
        born_date = [int(x) for x in born_date]
        if current_date >= born_date:
            if current_date[2] - born_date[2] > 0:
                end_age = f"{current_date[2] - born_date[2]} il {current_date[1] - born_date[1]} ay {current_date[0] - born_date[0]} gün"
            elif current_date[1] - born_date[1] > 0:
                end_age = f"{current_date[2] - born_date[2]} il {current_date[1] - born_date[1]} ay {current_date[0] - born_date[0]} gün"
            elif current_date[0] - born_date[0] > 0:
                end_age = f"{current_date[2] - born_date[2]} il {current_date[1] - born_date[1]} ay {current_date[0] - born_date[0]} gün"
            elif current_date[1] - born_date[1] == 0:
                 end_age = f"{current_date[2] - born_date[2]} il {current_date[0] - born_date[0]} gün"
            elif current_date[0] - born_date[0] == 0:
                end_age = f"{current_date[1] - born_date[1]} ay {current_date[0] - born_date[0]} gün"
        else:
            messages.error(request, "Tarix düzgün seçilməyib!")
            return redirect("home")
        if form.is_valid():
            form.instance.age = end_age
            form.save()
            return redirect("home")
        else:
            context["form"] = form
            context['data'] = object
            return render(request, "home.html", context)
    else:
        form = RegisterForm()
        context["form"] = form
        context['data'] = object
        return render(request, "home.html", context)


def TableView(request):
    form = RegisterForm()
    context["form"] = form
    return redirect("/table")


def EditView(request, pk,):
    edit = InfoFields.objects.filter(id=pk).last()
    if request.method == "POST":
        form = EditForm(request.POST, instance=edit)
        born_date = request.POST.get('age').split("/")
        born_date = [int(x) for x in born_date]
        if current_date >= born_date:
            if current_date[2] - born_date[2] > 0:
                end_age = f"{current_date[2] - born_date[2]} il {current_date[1] - born_date[1]} ay {current_date[0] -born_date[0]} gün"
            elif current_date[1] - born_date[1] == 0:
                end_age = f"{current_date[2] - born_date[2]} il {current_date[0] - born_date[0]} gün"

        else:
            messages.error(request, "Tarix düzgün seçilməyib!")
            return redirect("/home")
        if form.is_valid():
            form.instance.age = end_age
            form.save()
            return redirect("home")
        # else:
        #     context["form"] = form
        #     context['data'] = edit
        #     return render(request, "home.html", context)
    else:
        form = EditForm(instance=edit)
    context = {
        'form': form,
        'object': edit
    }
    return render(request, 'edit.html', context)

def AverageView(request, pk):
    month = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avqust', 'Sentyabr', 'Oktyabr', 'Noyabr', 'Dekabr']
    context['month'] = month

    # date = InfoFields.objects.filter(id=pk).last()
    # print(date)
    result = []
    for m in range(1,13):
        obj = {}
        obj["name"] = month[m-1]
        query = InfoFields.objects.filter(publish_date__month=m, publish_date__year=2019)
        if query:
            obj["data"] = query.values("weight").aggregate(Sum("weight"))["weight__sum"]/query.count()
            print(month[m-1],obj["data"])
        else:
            obj["data"] = None
        result.append(obj)
    print(result)
    return render(request, "average.html", context)
