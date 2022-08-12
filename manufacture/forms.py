from django import forms
from django.forms import SelectDateWidget
from .models import *


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-conntrol'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-conntrol'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_accountant', 'is_cashier')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SaleForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for myField in self.fields:
    #         self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Sale
        fields = ('date', 'client', 'model', 'size', 'quantity', 'price', 'total')

    date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class DailyProductionForm(forms.ModelForm):
    class Meta:
        model = DailyProduction
        fields = ('date', 'catalogue', 'quantity', 'package', 'defect_worker', 'defect_machine', 'defect_saya')

    date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))


class CatalogueForm(forms.ModelForm):
    class Meta:
        model = Catalogue
        fields = '__all__'


class DailyTimesheetForm(forms.ModelForm):

    class Meta:
        model = DailyTimesheet
        fields = ['date', 'employee', 'stanok', 'rate', 'daily_prod_quant']

    date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))

