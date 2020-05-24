import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage
from house.models import Category, House, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = House.objects.all()[:6]
    category = Category.objects.all()
    dayhouses = House.objects.all()[:4]
    randomhouses = House.objects.all().order_by('?')[:4]

    context = {'setting': setting,
               'category': category,
               'page':'home',
               'sliderdata': sliderdata,
               'dayhouses': dayhouses,
               'randomhouses': randomhouses
               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    context = {'setting': setting,
               'category': category,
               'page':'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    context = {'setting': setting,
               'category': category,
               'page':'referanslar'}
    return render(request, 'referanslar.html', context)


def iletisim(request):
    category = Category.objects.all()
    if request.method == 'POST':  # form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'category': category, 'form': form}
    return render(request, 'iletisim.html', context)

def category_houses(request, id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    houses = House.objects.filter(category_id=id)
    context = {'houses' : houses,
               'categorydata': categorydata,
               'category': category
               }
    return render(request, 'evler.html', context)


def house_detail(request, id, slug):
    category = Category.objects.all()
    house = House.objects.get(pk=id)
    images = Images.objects.filter(house_id=id)
    comments = Comment.objects.filter(house_id=id, status= 'True')
    contenthouses = House.objects.all()[:4]

    context = {'house': house,
                'category': category,
               'images' : images,
               'comment' : comments,
               'contenthouses': contenthouses
               }
    return render(request, 'house_detail.html', context)

def house_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            houses = House.objects.filter(title__icontains=query)
            context = {
                'category': category,
                'houses': houses,
            }
            return render(request, 'house_search.html', context)
    return HttpResponseRedirect('/')

def house_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        house = House.objects.filter(title__icontains=q)
        results = []
        for rs in house:
            house_json = {}
            house_json = rs.title
            results.append(house_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası ! Kullanıcı adı ya da şifre yanlış")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'signup.html', context)