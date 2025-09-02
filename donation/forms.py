from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Donation, BloodRequest

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=True)
    mobile = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500'
            })



class DonationForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Donation
        fields = "__all__"
        exclude = ["user"]


class BloodRequestForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = BloodRequest
        fields = "__all__"
        exclude = ["user"]

