from django.urls import include, path
from . import views
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'zips', views.ZipViewSet, basename = 'zips')
# router.register(r'cities', views.CityViewSet, basename = 'cities')

urlpatterns = [
    #path("vue", views.vue_page, name='vue_page'),
    #path("vue_cities", views.vue_page, name='vue_cities_page'),
    #path("vanilla", views.vanilla_page, name='vanilla_page'),
    #path("vanilla_cities", views.vanilla_cities_page, name='vanilla_cities_page'),
    #path("", include(router.urls)),
    path('get-province', views.getProvince, name='get-province'),
    path('get-cities', views.getCities, name='get-cities'),
    path('process-form', views.processForm, name='process-form'),
    path('countries', views.load_form, name='load-form'),
]
