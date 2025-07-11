from django import forms
# from .models import Address
from django.conf import settings
from .countries_handler import return_state_by_country, return_city_by_state
from django.utils.translation import gettext_lazy as _

# PUT forms.ModelForm TO ASSOCIATE THE FORM WITH A MODEL
class AddressForm(forms.Form):
    """ Using an empty list as a default argument is a common error. 
    It may lead to unwanted behavior. The correct way to do it is to 
    initialize the list to None """
    def __init__(self, data=None, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        if data is not None:
            self.fields['country'].choices = data

    country = forms.ChoiceField(
        choices = (),#arr_country,
        required = False, 
        label=_('Company Country Location'), 
        widget=forms.Select(attrs={'class':'form-control', 'id': 'id_country'}),
    )

    def get_state_by_country(self, country, lng):
        return return_state_by_country(country, lng)

    def get_city_by_state(self, state, lng):
        return return_city_by_state(state, lng)

    class Meta:
        # model = Address
        fields = ['country']
