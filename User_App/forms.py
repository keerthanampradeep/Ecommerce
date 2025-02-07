from django import forms
from .models import DeliveryAddress
from Admin_App.models import Category  #
from User_App.models import Item    # Import Item model from your User_App



class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = [ 'phone_number', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country']
class SearchForm(forms.Form):
    query = forms.CharField(required=False, label="Search Products and Categories", max_length=100)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Category")


class SubscribeForm(forms.Form):
    email = forms.EmailField()