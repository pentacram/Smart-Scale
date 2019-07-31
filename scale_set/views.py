from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.utils import timezone
import datetime
from .forms import *
from .models import *
from django.db.models import Q

from datetime import date

from django.views.generic.dates import MonthArchiveView



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
    # data = InfoFields.objects.all()
    form = RegisterForm()
    pagination = Paginator(object, 10)
    all_objects = pagination.get_page(request.GET.get('page', 1))
    context["page_list"] = all_objects
    context["page_range"] = pagination.page_range
    if request.method == "POST":
        form = RegisterForm(request.POST)
        form.instance.username = request.user

        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            context["form"] = form
            context['data'] = object
            return render(request, "home.html", context)
    else:
        form = RegisterForm()
        if request.GET.get('daterange'):
            all = request.GET.get('daterange').replace(" ", '')
            start = all[:10].replace('/', '-')
            end = all[11:].replace('/', '-')
            objects_by_date = InfoFields.objects.filter(born_date__range=[start, end])
            context['objects'] = objects_by_date

        context["form"] = form
        context['data'] = object
        return render(request, "home.html", context)


def TableView(request):
    form = RegisterForm()
    context["form"] = form
    return redirect("/table")


def EditView(request, pk, ):
    edit = InfoFields.objects.filter(id=pk).last()
    if request.method == "POST":
        form = EditForm(request.POST, instance=edit)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EditForm(instance=edit)
    context = {
        'form': form,
        'object': edit
    }
    return render(request, 'edit.html', context)


def AverageView(request):
    # obj={}
    month = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avqust', 'Sentyabr', 'Oktyabr', 'Noyabr',
             'Dekabr']
    context['month'] = month

    result = []

    for m in range(1, 13):

        obj = {}

        obj["name"] = month[m - 1]
        query = InfoFields.objects.filter(publish_date__month=m, publish_date__year=2019)
        if query:
            obj["data1"] = (query.values("weight").aggregate(Sum("weight"))["weight__sum"] // query.count())
            # print(month[m-1], obj["data1"])
        else:
            obj["data1"] = None
        result.append(obj)
        context['result'] = result
    # print(result)
    return render(request, "average.html", context)


def DeleteView(request, id):
    delete = InfoFields.objects.filter(id=id).last()
    context["delete"] = delete
    if request.method == 'POST':
        delete.delete()
        return redirect('home')

    return render(request, "home.html", context)


#
def SearchView(request, id):
    if q in request.GET:
        query = request.GET('q')
        context["search"] = InfoFields.objects.filter(publish_date__range=query)
