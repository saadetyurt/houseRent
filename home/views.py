from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage
from house.models import Category, House


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
