from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254)
    password2 = forms.CharField(widget=forms.PasswordInput(
    ), label='Confirm')

    def clean_username(self):
        username = self.cleaned_data['username']
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')


class Appuserform(forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+91'. Up to 15 digits allowed.")
    mobile = forms.CharField(max_length=12, min_length=10, validators=[
                             phone_regex], widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Appuser
        fields = ['mobile']


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['pimg', 'pname', 'company', 'price',
                  'category', 'website', 'specification']
