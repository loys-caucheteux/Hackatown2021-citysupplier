from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import userBase, magBase
from .forms import RegisterForm, ParagraphErrorList, LoginForm, RegisterMagForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from . import funcs
import folium
from folium.plugins import BeautifyIcon
from django.contrib.auth import logout
from django.views.generic import TemplateView
import os
from django.conf import settings
from django.conf.urls.static import static
from django.db import IntegrityError, transaction
from branca.element import Figure

# Create your views here.
def index(request):
    try:
        a = request.session['logged']
    except KeyError:
        request.session['logged'] = False
    try:
        if request.GET['logout']:
            logout(request)
            request.session['logged'] = False
    except KeyError:
        a = 0  
    template = loader.get_template('map/index.html')
    return HttpResponse(template.render(request=request))

def register(request):
    try:
        a = request.session['logged']
    except KeyError:
        request.session['logged'] = False
    if request.session['logged'] == False:
        if request.method == 'POST':
            form = RegisterForm(request.POST, error_class=ParagraphErrorList)
            if form.is_valid():
                email = form.cleaned_data['mail']
                pwd = form.cleaned_data['pwd']
                name = form.cleaned_data['name']
                surname = form.cleaned_data['surname']
                adress = form.cleaned_data['adress']
                latitude=funcs.getlat_fadress(adress)
                longitude=funcs.getlon_fadress(adress)
                if latitude == 1084 and longitude == 1084:
                    context = {
                        'form' : RegisterForm(),
                        'adress': True
                        }
                    return render(request, 'map/register.html', context)
                user = userBase.objects.filter(mail=email)
                if not user.exists():
                    user = userBase.objects.create(
                        name=name,
                        surname=surname,
                        mail=email,
                        pwd=pwd,
                        adress=adress,
                        lat=funcs.getlat_fadress(adress),
                        lon=funcs.getlon_fadress(adress)
                    )
                    return render(request, 'map/index.html')
                else:
                    context = {
                        'form' : RegisterForm(),
                        'used': True
                        }
                    return render(request, 'map/register.html', context)
            else:
                context['errors'] = form.errors.items()
        else:
            form = RegisterForm()
    else:
        return render(request, 'map/access.html')
    context = {'form' : RegisterForm()}
    return render(request, 'map/register.html', context)

def login(request):
    f = 0
    try:
        a = request.session['logged']
    except KeyError:
        request.session['logged'] = False
    if request.session['logged'] == False:
        if request.method == 'POST':
            form = LoginForm(request.POST, error_class=ParagraphErrorList)
            if form.is_valid():
                email = form.cleaned_data['mail']
                pwd = form.cleaned_data['pwd']
                try:
                    with transaction.atomic():
                        user = userBase.objects.filter(mail=email)
                except IntegrityError:
                    form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."
                    f = 1
                if  f != 1 and user.exists():
                    try:
                        getpwd = user.get(pwd=pwd)
                    except ObjectDoesNotExist:
                        context = {'form' : LoginForm(), 'fail' : True}
                        return (render(request, 'map/login.html', context))
                    request.session['logged'] = True
                    request.session['name'] = getpwd.name
                    request.session['surname'] = getpwd.surname
                    request.session['mail'] = getpwd.mail
                    return (render(request, 'map/index.html'))
                else:
                    context = {'form' : LoginForm(), 'fail' : True}
                    return (render(request, 'map/login.html', context))
            else:
                context['errors'] = form.errors.items()
        else:
            form = LoginForm()
    else:
        return render(request, 'map/access.html')
    context = {
        'form' : LoginForm(),
        'fail' : False
    }
    return render(request, 'map/login.html', context)

def registerMag(request):
    try:
        a = request.session['logged']
    except KeyError:
        request.session['logged'] = False
    if request.session['logged']:
        if request.method == 'POST':
            form = RegisterMagForm(request.POST, error_class=ParagraphErrorList)
            if form.is_valid():
                name = form.cleaned_data['name']
                adress = form.cleaned_data['adress']
                user = userBase.objects.filter(mail=request.session['mail'])
                getuser = user.get(mail=request.session['mail'])
                lat = funcs.getlat_fadress(adress)
                lon = funcs.getlon_fadress(adress)
                mag = magBase.objects.filter(lat=lat, lon=lon)
                if not mag.exists():
                    mag = magBase.objects.create(
                        name=name,
                        user=getuser,
                        lat=lat,
                        lon=lon,
                        adress=adress
                    )
                    return render(request, 'map/index.html')
                else:
                    context = {
                        'form' : RegisterMagForm(),
                        'used': True
                        }
                    return render(request, 'map/registerMag.html', context)
            else:
                context['errors'] = form.errors.items()
        else:
            form = RegisterMagForm()
    else:
        return render(request, 'map/access.html')
    context = {'form' : RegisterMagForm()}
    return render(request, 'map/registerMag.html', context)


def show_map(request):
    #creation of map comes here + business logic
    try:
        a = request.session['logged']
    except KeyError:
        request.session['logged'] = False
    if request.session['logged']:
        user = userBase.objects.filter(mail=request.session['mail']).get()
        store = magBase.objects.values_list('adress', flat=True)
        store = list(store)
        m = folium.Map(
            location=[user.lat, user.lon],
            zoom_start=15,
            tiles='Stamen Terrain',
            min_zoom=8,
            width=1200, height=600
        )
        folium.TileLayer('openstreetmap').add_to(m)
        number_icon = BeautifyIcon(icon='angle-double-down', icon_shape='marker',text_color="#000", border_color="transparent",
            background_color="#22F", inner_icon_style="font-size:12px;padding-top:-5px;") 
        folium.Marker(
            location=[user.lat, user.lon],
            popup=folium.Popup(str(user.adress+'\nChez vous'), width=200),
            icon=number_icon).add_to(m)
        for item in store:
            mag = magBase.objects.filter(adress=item).first()
            number_icon = BeautifyIcon(icon='angle-double-down', icon_shape='marker',text_color="#000", border_color="transparent",
            background_color="#2D2", inner_icon_style="font-size:12px;padding-top:-5px;") 
            folium.Marker(
                location=[funcs.getlat_fadress(item), funcs.getlon_fadress(item)],
                popup=folium.Popup(str(item + '\n' + mag.name), width=200),
                icon=number_icon).add_to(m)
        m=m._repr_html_() #updated
        context = {'my_map': m}
        return render(request, 'map/map.html', context)
    else:
        return render(request, 'map/access.html')
