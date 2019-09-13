from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import *
from .models import *


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
    a = [str(x.number) for x in InfoFields.objects.all()]
    a = set(a)
    object = [InfoFields.objects.filter(number=e).last() for e in a]
    form = RegisterForm()
    pagination = Paginator(object, 10)
    all_objects = pagination.get_page(request.GET.get('page', 1))
    context["page_list"] = all_objects

    context["objects"] = [InfoFields.objects.filter(number=e).last() for e in a]

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
            objects_by_date = InfoFields.objects.filter(publish_date__range=[start, end])
            context['objects'] = objects_by_date
        else:
            context['objects'] = all_objects
        context["form"] = form
        context['data'] = object
        return render(request, "home.html", context)


def TableView(request):
    form = RegisterForm()
    context["form"] = form
    return redirect("/table")


def EditView(request, pk):
    edit = InfoFields.objects.filter(id=pk).last()
    print(edit.weight)
    context['form'] = EditForm(instance=edit)
    if request.method == "POST":
        form = EditForm(request.POST, instance=edit)
        if form.is_valid():
            form.save()

            return redirect("home")


    context['object']=edit

    return render(request, 'edit.html', context)




def AverageView(request,id):
    # obj={}
    month = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avqust', 'Sentyabr', 'Oktyabr', 'Noyabr',
             'Dekabr']
    context['month'] = month

    result = []

    for m in range(1, 13):

        obj = {}

        obj["name"] = month[m - 1]
        query = InfoFields.objects.filter(number=id, publish_date__month=m, publish_date__year=2019)
        if query:
            sum=0
            for x in query:
                sum += x.weight
            total=sum//query.count()
            obj["data1"] = total
            # print(month[m-1], obj["data1"])
        else:
            obj["data1"] = '-'
        result.append(obj)
        context['result'] = result
        context['id'] = id
    # print(result)
    return render(request, "average.html", context)

def AllDataView(request,id=1, month='September'):
    month_list = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avqust', 'Sentyabr', 'Oktyabr', 'Noyabr',
             'Dekabr']

    # result = []

    month_num = month_list.index(month) + 1
    # num=0
    # for m in range(1, 13):
    #     if month_list[m - 1] == month:
    #         num=m
    # print(num)
    query = InfoFields.objects.filter(number=id, publish_date__month=month_num, publish_date__year=2019)
    context['all_data'] = query
    return render(request, "all_data.html", context)


def DeleteView(request, id):
    delete = InfoFields.objects.filter(id=id).last()
    context["delete"] = delete
    if request.method == 'POST':
        delete.delete()
        return redirect('home')

    return render(request, "home.html", context)


