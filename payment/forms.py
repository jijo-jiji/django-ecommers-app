from django import forms 
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_fullname = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'FullName'}),required=True)
    shipping_email = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),required=True)
    shipping_address1 = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address1'}),required=True)
    shipping_address2 = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address2'}),required=True)
    shipping_city = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}),required=True)
    shipping_state = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}),required=True)
    shipping_zipcode =forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Zipcode'}),required=True)
    shipping_country = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}),required=True)
    
    class Meta:
        model = ShippingAddress
        fields = ['shipping_fullname','shipping_email','shipping_address1','shipping_address2','shipping_city','shipping_state','shipping_zipcode','shipping_country']
        
        exclude =['user',]
        
class PaymentForm(forms.Form):
    card_name = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name on card'}),required=True)
    card_number = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card number'}),required=True)
    card_exp_date = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Expiration Date'}),required=True)
    card_cvv_number = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'CVV Code'}),required=True)
    card_address1 = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing address1'}),required=True)
    card_address2 = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing address2'}),required=False)
    card_city = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing city'}),required=True)
    card_state = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing state'}),required=True)
    card_zipcode = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing zipcode'}),required=True)
    card_country = forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing country'}),required=True)
    