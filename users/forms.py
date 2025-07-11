from django.contrib.auth.forms import UserCreationForm
# we are using a customized user model therefore we need to call get_user_model
from django.contrib.auth import get_user_model
from django.forms.fields import BooleanField
from django.utils.translation import gettext, gettext_lazy as _
from django import forms
from django.contrib.auth import forms as auth_forms
from .models import User as CustomUser
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from django import forms
from .models import DispositivoInventario

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = DispositivoInventario
        fields = '__all__'
        exclude = ['creado_por', 'fecha_creacion']
        widgets = {
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date'}),
        }











class CustomUserCreationForm(UserCreationForm):
        
    class Meta(UserCreationForm.Meta):
        # the user model was customized it should be invoked
        model = get_user_model()
        """
        The fields accepts a list or tuple of field names you want to show in the form. If you want to show all the fields just use "__all__" (that's double underscore). 
        fields = '__all__'
        The required fields like username and password are always shown. This array is also important to describe the order of which the fields will
        be shown in the form.
        """
        fields = UserCreationForm.Meta.fields + ("email","email2")
    
    #forms.EmailField.widget.attrs.pop("autofocus", None)
    # email2 is not part of the model and will not be persisted. For this 
    # reason we are creating a new field using forms and not ModelForm
    email2 = forms.EmailField(
        label=_("Re-Type Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'off'})
    )

    accept_read_terms = forms.BooleanField(required=False)
    # mark_safe is necessary to ensure the link is rendered and not hardcoded. 
    # Without it, the actual HTML would be rendered and this is incorrect most 
    # of the time.
    accept_read_terms.label = mark_safe(_("I accept the ")+"<a href='terms.html'>" +_("terms")+"</a>")

    """ This is the correct way to make custom validations. clean_<field> will be called after the form has been submitted and after the other validations from Django have been made. 
    Django also accept a general clean() method wich apply to the entire form. But error messages would be displayed above the entire form instead than above the erroneous field. 
    """
    def clean_email2(self):
        email1 = self.cleaned_data['email']
        email2 = self.cleaned_data['email2']
        error_messages = {
        'email_mismatch': _('Email and Re-Type email must be the same.'),
        }
        if email1 != email2:
            raise ValidationError(
                error_messages['email_mismatch'],
                        code='email_mismatch',
            )
    
    def clean_accept_read_terms(self):
        error_messages = {
            'accept_terms': _('You must accept the terms and conditions.'),
        }
        art = self.cleaned_data['accept_read_terms']
        if art is False:
            raise ValidationError(
                error_messages['accept_terms'], code='accept_terms',
            )


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = CustomUser
        fields = '__all__'

# This is just a test form to test email connectivity
class ContactMeForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter first name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter last name'}), required=True)
    emailid = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter email'}), required=True)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter phone number'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter subject'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter Message'}), required=True)
