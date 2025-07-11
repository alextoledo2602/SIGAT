from rest_framework import serializers
# from .models import Zip, Cities, States, Countries

#This will convert python QuerySets to JSON format which is what  will be served to the front end. There are other ways to do this, but for the sake of learning we will use the Serializers and Rest Framework.
class ZipSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Zip
        fields = '__all__'


# Fields: 'name','country','country-code','fips_code','iso2','latitude','longitude','created_at','updated_at','flag','wikidataid'
class StatesSerializer(serializers.ModelSerializer):    
    class Meta:
        # model = States
        fields = ['name', 'iso2']

# Fields 'name','iso3','iso2','phonecode','capital','currency_symbol','tld','native','region','subregion','timezones','translations','latitude','longitude','emoji','emojiu','created_at','updated_at','flag','wikidataid'
class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Countries
        fields = ['name', 'iso2', ]#'translations']


#Fields: 'name','state','state_code','country','country_code','latitude','longitude','created_at','updated_at','flag','wikidataid'
class CitiesSerializer(serializers.ModelSerializer):
    state = StatesSerializer(many=False)
    country = CountriesSerializer(many=False)

    class Meta:
        # model = Cities
        fields = ['name', 'state', 'country', 'latitude', 'longitude']

