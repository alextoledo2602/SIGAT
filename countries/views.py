from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .forms import AddressForm
# from .models import Zip, Countries, States, Cities
# from .serializers import ZipSerializer, CitiesSerializer, StatesSerializer, CountriesSerializer
# from rest_framework import viewsets
import requests, json
from django.utils.translation import gettext as gt
from django.utils.translation import gettext_lazy as _, get_language
from .countries_handler import get_country, return_state_by_country
from pprint import pprint
from inspect import getmembers

def getProvince(request):
    # country = request.POST.get('country')
    #from django.http import HttpResponse
    #print(HttpResponse(request.POST.items()))
    country = json.load(request)['country']
    af = AddressForm()
    provinces = af.get_state_by_country(country, get_language())
    return JsonResponse({'provinces': provinces})

def getCities(request):
    # province = request.POST.get('province')
    province = json.load(request)['province']
    af = AddressForm()
    cities = af.get_city_by_state(province, get_language())
    return JsonResponse({'cities': cities})

def processForm(request):
    context = {}    
    if request.method == 'GET':
        form  = AddressForm()
        context['form'] = form
        return render(request, 'address.html', context)    
        
    if request.method == 'POST':
        form  = AddressForm(request.POST)
        if form.is_valid():
            selected_province = request.POST['state']
            obj = form.save(commit=False)
            obj.state = selected_province
            obj.save()

def load_form(request):
    # get_language must be called here, if you call it in country_handler or 
    # in forms.py, it will return the default language when the server 
    # started and not when the request was sent (with new lng in the url)
    arr_country = get_country(get_language())
    form = AddressForm(arr_country)
    return render(request, 'countries/country_form.html', {'form':form, 'lang':get_language()})

"""
##### OLD STUFF #####
def vue_page(request):
    if request.method == "GET":
        return render(request, "vue-page.html")


def vanilla_page(request):
    if request.method == "GET":
        return render(request, "vanilla-page.html")


def vue_cities_page(request):
    if request.method == "GET":
        return render(request, "vue-cities-page.html")


The response should be, for 24.48.0.1
    Location {'status': 'success', 'country': 'Canada', 'countryCode': 'CA', 'region': 'QC', 'regionName': 'Quebec', 'city': 'Montreal', 'zip': 'H1K', 'lat': 45.6085, 'lon': -73.5493, 'timezone': 'America/Toronto', 'isp': 'Le Groupe Videotron Ltee', 'org': 'Videotron Ltee', 'as': 'AS5769 Videotron Telecom Ltee', 'query': '24.48.0.1'}

    The docu is here https://ip-api.com/docs/api:json
"""
"""
def vanilla_cities_page(request):
    req = requests.get("http://ip-api.com/json/"+request.META.get('REMOTE_ADDR'))
    # data refers to geolocation not country names
    data = json.loads(req.text)
    if request.method == "GET":
        return render(request, "vanilla-cities-page.html", {'ip_geoloc': data})

class ZipViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ZipSerializer
    
    def get_queryset(self):
        zip_code = self.request.query_params.get("zip_code")
        queryset = Zip.objects.filter(
            zip_code__startswith=zip_code
        )[:6] # [:6] means that the query is limited to six objects
        return queryset


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitiesSerializer
    
    #
    # Option 1 raw query
    # SELECT 1 AS id is required by Django but not necessary for the query
    # queryset = Cities.objects.raw("SELECT 1 as id, cities.name as ci, states.name as s, countries.name as co FROM cities JOIN states ON states.id = cities.state_id LEFT OUTER JOIN countries ON countries.id = states.country_id WHERE cities.name = %s", [city])
    #
    # Option 2 with normal queryset
    def get_queryset(self):
        city = self.request.query_params.get("cityname")
        #city = "Guadalajara"
        queryset = Cities.objects.filter(name__startswith=city)
        #queryset[1].name will contain "Madrid"
        #queryset[1].country.name will contain "Spain"
        #queryset[1].state.name will contain "Madrid"
        #queryset should be iterated then
        return queryset
"""