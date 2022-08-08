from django import forms
from django.forms import SelectDateWidget
from .models import *


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['date', 'client', 'model', 'size', 'quantity', 'price', 'total']

    date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'address', 'file']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['occupation', 'fio', 'phone', 'phone1', 'monthly_salary', 'active', 'date_start']


class DailyProductionForm(forms.ModelForm):
    class Meta:
        model = DailyProduction
        fields = ['date', 'catalogue', 'quantity', 'package', 'defect_worker', 'defect_machine', 'defect_saya']

    date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))
    # quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'row'}))


class CatalogueForm(forms.ModelForm):
    class Meta:
        model = Catalogue
        fields = ['model', 'code', 'color', 'image', 'size']


class DailyTimesheetForm(forms.ModelForm):
    class Meta:
        model = DailyTimesheet
        fields = ['date', 'employee', 'rate', 'daily_prod_quant', 'rate_day', 'machine_tool']

    date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))

