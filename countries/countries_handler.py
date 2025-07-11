from django.utils.translation import gettext_lazy as _, get_language
import importlib
import json

def readJson(filename):
    with open(filename, 'r', encoding="utf8") as fp:
        return json.load(fp)

def get_country(current_lng):
    imp = importlib.import_module("countries.translations.countries_%s" % current_lng)
    filepath = 'myproj/static/data/countries_states_cities.json'
    all_data = readJson(filepath)

    all_countries = [('----', _("-- Select a Country --"))]

    for x in all_data:
        y = (x['name'], imp.t_countries(x['name']))
        all_countries.append(y)

    all_countries.sort(key = lambda x: x[1])
    return all_countries

def return_state_by_country(country, current_lng):
    """ GET STATE SELECTION BY COUNTRY INPUT """
    imp = importlib.import_module("countries.translations.countries_%s" % current_lng)
    filepath = 'myproj/static/data/countries_states_cities.json'
    all_data = readJson(filepath)

    all_states = []

    for x in all_data:
        if x['name'] == country:
            if 'states' in x:
                for state in x['states']:
                    y = (state['name'], imp.t_countries(state['name']))
                    all_states.append(y)
            else:
                all_states.append(country)
    
    return all_states

def return_city_by_state(state, current_lng):
    """ GET CITY SELECTION BY STATE INPUT """
    imp = importlib.import_module("countries.translations.countries_%s" % current_lng)
    filepath = 'myproj/static/data/countries_states_cities.json'
    all_data = readJson(filepath)

    all_cities = []

    for x in all_data:
        for stat in x['states']:
            if stat['name'] == state:
                # print("found state")
                if 'cities' in stat:
                    # print("This country has cities")
                    for city in stat['cities']:
                        y = (city['name'], imp.t_countries(city['name']))
                        all_cities.append(y)
                else:
                    all_cities.append(state)    
    return all_cities
