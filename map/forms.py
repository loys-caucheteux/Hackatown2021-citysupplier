from django import forms
from django.forms.utils import ErrorList

class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])

class RegisterForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    surname = forms.CharField(
        label='Surname',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    adress = forms.CharField(
        label='Adresse sous la forme <Numéro> <Rue> <Code Postal>',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    mail = forms.EmailField(
        label='Email',
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
        )
    pwd = forms.CharField(
        label='Password',
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )

class LoginForm(forms.Form):
    mail = forms.EmailField(
        label='Email',
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
        )
    pwd = forms.CharField(
        label='Password',
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )

class RegisterMagForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    adress = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )