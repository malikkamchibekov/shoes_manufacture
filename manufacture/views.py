from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime
from django.db.models import Sum, Count
import datetime
import pandas as pd
from django_pandas.io import read_frame
import numpy as np


def index(request):
    return render(request, 'manufacture/index.html')


# отображение ежемесячной выработки
def monthly_production(request):
    error = False
    if 'q1' and 'q2' in request.GET:
        q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
        q2 = datetime.datetime.strptime(request.GET['q2'], '%Y-%m-%d')

        if not q1:
            error = True
        elif not q2:
            error = True
        else:
            item = DailyProduction.objects.filter(date__range=(q1, q2))
            # cat_model = Catalogue.objects.values('model')
            # cat_code = Catalogue.objects.values('code')
            # cat_color = Catalogue.objects.values('color')
            # df = read_frame(item)
            # df = read_frame(item, fieldnames=['date', 'quantity', 'catalogue', 'package', 'defect_worker'])
            rows = ['date']
            cols = ['catalogue']

            pt = item.to_pivot_table(values='quantity', rows=rows, cols=cols, aggfunc=np.sum, fill_value=0, margins=True)
            context = {
                "df": pt.to_html(),
            }

            return render(request, 'manufacture/monthly_production.html', context)
    return render(request, 'manufacture/monthly_production.html', {'error': error})


# Продажи общие
def salary_total(request):
    sales = Sale.objects.all().order_by('-pk')
    return render(request, 'manufacture/salary_total.html', {'sales': sales})


# Изменение значений в продажах
def edit_sale(request, id):
    try:
        edited_sale = Sale.objects.get(id=id)

        if request.method == "POST":
            edited_sale.vendor_code = request.POST.get("vendor_code")
            edited_sale.title = request.POST.get("title")
            edited_sale.type = request.POST.get("type")
            edited_sale.size = request.POST.get("size")
            edited_sale.quantity = request.POST.get("quantity")
            edited_sale.price = request.POST.get("price")
            edited_sale.total = request.POST.get("total")
            edited_sale.save()
            return redirect('salary_total')
        else:
            return render(request, "manufacture/edit_sale.html", {"edited_sale": edited_sale})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Продажа не найдена</h2>")


# удаление продаж из бд
def delete_sale(request, id):
    try:
        deleted_sale = Sale.objects.get(id=id)
        deleted_sale.delete()
        return redirect('salary_total')
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Продажа не найдена</h2>")


# добавление продаж по форме модели
def add_new_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            try:
                sale = form.save()
                sale.fetch_total()
                sale.save()
                return redirect('sales')
            except:
                form.add_error(None, "Что-то пошло не так, попробуйте снова")
        else:
            form = SaleForm()
    else:
        form = SaleForm()
    return render(request, 'manufacture/new_sale.html', {'form': form})


# отображение каталога
def view_catalogue(request):
    catalogue = Catalogue.objects.all()
    return render(request, 'manufacture/catalogue.html', {'catalogue': catalogue})


# добавление нового продукта в каталог
def add_new_product(request):
    if request.method == 'POST':
        form = CatalogueForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save()
                product.save()
                return redirect('catalogue')
            except:
                form.add_error(None, "Что-то пошло не так, попробуйте снова")
        else:
            form = CatalogueForm()
    else:
        form = CatalogueForm()
    return render(request, 'manufacture/new_product.html', {'form': form})


# добавление нового клиента
def add_new_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            try:
                client = form.save()
                client.save()
                return redirect('clients')
            except:
                form.add_error(None, "Что-то пошло не так, попробуйте снова")
        else:
            form = ClientForm()
    else:
        form = ClientForm()
    return render(request, 'manufacture/new_client.html', {'form': form})


# отображение списка клиентов
def view_client(request):
    clients = Client.objects.all()
    return render(request, 'manufacture/clients.html', {'clients': clients})


# добавление нового сотрудника
def add_employer(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.save()
            return redirect('employers')
        else:
            form = EmployeeForm()
    else:
        form = EmployeeForm()
    return render(request, 'manufacture/new_employer.html', {'form': form})


# отображение списка сотрудников
def employers(request):
    employer = Employee.objects.all()
    return render(request, 'manufacture/emp_report.html', {'employer': employer})


# отображение ежедневной выработки
def view_daily_production(request):
    error = False
    if 'q1' in request.GET:
        q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
        if not q1:
            error = True
        else:
            production = DailyProduction.objects.filter(date=q1)
            total_quantity = DailyProduction.objects.filter(date=q1).aggregate(TOTAL=Sum('quantity'))['TOTAL']
            total_package = DailyProduction.objects.filter(date=q1).aggregate(TOTAL=Sum('package'))['TOTAL']
            total_defect_worker = DailyProduction.objects.filter(date=q1).aggregate(TOTAL=Sum('defect_worker'))['TOTAL']
            total_defect_machine = DailyProduction.objects.filter(date=q1).aggregate(TOTAL=Sum('defect_machine'))[
                'TOTAL']
            total_defect_saya = DailyProduction.objects.filter(date=q1).aggregate(TOTAL=Sum('defect_saya'))['TOTAL']

            context = {
                'q1': q1,
                'production': production,
                'total_quantity': total_quantity,
                'total_package': total_package,
                'total_defect_worker': total_defect_worker,
                'total_defect_machine': total_defect_machine,
                'total_defect_saya': total_defect_saya,
            }
            return render(request, 'manufacture/daily_production.html', context)

    return render(request, 'manufacture/daily_production.html', {'error': error})


# добавление ежедневки
def add_daily_production(request):
    if request.method == 'POST':
        form = DailyProductionForm(request.POST)
        if form.is_valid():
            try:
                daily_production_form = form.save()
                daily_production_form.fetch_package()
                daily_production_form.save()
                return redirect('daily_production')
            except:
                form.add_error(None, "Что-то пошло не так, попробуйте снова")
        else:
            form = DailyProductionForm()
    else:
        form = DailyProductionForm()
    return render(request, 'manufacture/new_daily_production.html', {'form': form})


# добавление ежедневного табеля сотрудников
def add_daily_timesheet(request):
    if request.method == 'POST':
        form = DailyTimesheetForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('daily_timesheet2')
            except:
                form.add_error(None, "Что-то пошло не так, попробуйте снова")
        else:
            form = DailyTimesheetForm()
    else:
        form = DailyTimesheetForm()
    return render(request, 'manufacture/new_daily_timesheet.html', {'form': form})


# поиск по Эва
def search(request):
    error = False
    if 'q1' and 'q2' in request.GET:
        q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
        q2 = datetime.datetime.strptime(request.GET['q2'], '%Y-%m-%d')

        if not q1:
            error = True
        elif not q2:
            error = True
        else:
            quantities = DailyProduction.objects.filter(date__range=(q1, q2))
            emp = Employee.objects.all()
            return render(request, 'manufacture/raschet_pu.html',
                          {'quantities': quantities,
                           'q1': q1,
                           'q2': q2,
                           'emp': emp}
                          )
    return render(request, 'manufacture/search_form.html', {'error': error})


# отображение ежедневного табеля сотрудников
def view_daily_timesheet(request):
    error = False
    if 'q1' in request.GET:
        q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
        if not q1:
            error = True
        else:
            timesheet = DailyTimesheet.objects.filter(date=q1)
            total_emp = DailyTimesheet.objects.filter(date=q1).count()
            context = {
                'timesheet': timesheet,
                'q1': q1,
                'total_emp': total_emp,
            }
            return render(request, 'manufacture/daily_timesheet2.html', context)

    return render(request, 'manufacture/daily_timesheet2.html', {'error': error})


def search_pu(request):
    error = False
    if 'q1' and 'q2' in request.GET:
        q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
        q2 = datetime.datetime.strptime(request.GET['q2'], '%Y-%m-%d')

        if not q1:
            error = True
        elif not q2:
            error = True
        else:
            quantities = DailyTimesheet.objects.filter(date__range=(q1, q2), stanok='ПУ')
            #item = DailyProduction.objects.filter(date__range=(q1, q2))
            # df = read_frame(item)
            # df = read_frame(item, fieldnames=['date', 'quantity', 'catalogue', 'package', 'defect_worker'])
            rows = ['employee', 'rate']
            cols = ['date']

            pt = quantities.to_pivot_table(
                values=['daily_prod_quant', 'rate_day'],
                rows=rows, cols=cols,
                aggfunc=np.sum,
                fill_value=0,
                margins=True
            )
            mydict = {
                "df": pt.to_html(),
                    }
            return render(request, 'manufacture/raschet_pu.html', mydict)
    return render(request, 'manufacture/raschet_pu.html', {'error': error})
