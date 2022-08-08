from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .forms import *
from datetime import datetime
from django_tables2 import SingleTableView, tables, RequestConfig
from django.db.models import Sum, Count
import datetime
from django.shortcuts import render
from .models import*
import pandas as pd
from django_pandas.io import read_frame
import numpy as np
#
# class DailyProductionTable(tables.Table):
#     class Meta:
#         model = DailyProduction
#
#
# class DailyProductionList(SingleTableView):
#     model = DailyProduction
#     paginate_by = 12
#     table_class = DailyProductionTable
#     template_name = "django_tables2/bootstrap.html"
#
#
# def view_daily_production(request):
#     table = DailyProductionTable(DailyProduction.objects.all())
#     model = DailyProduction
#     table_class = DailyProductionTable
#     RequestConfig(request).configure(table)
#     return render(request, 'manufacture/daily_production.html', {'table': table})



def index(request):
    return render(request, 'manufacture/index.html')


# Продажи общие
def sale_total(request):
    sales = Sale.objects.all().order_by('-pk')
    return render(request, 'manufacture/sale_total.html', {'sales': sales})


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
            return redirect('sale_total')
        else:
            return render(request, "manufacture/edit_sale.html", {"edited_sale": edited_sale})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Продажа не найдена</h2>")


# удаление продаж из бд
def delete_sale(request, id):
    try:
        deleted_sale = Sale.objects.get(id=id)
        deleted_sale.delete()
        return redirect('sale_total')
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
            try:
                form.save()
                return redirect('employers')
            except:
                form.add_error(None, "Что-то пошло не так, попробуйте снова")
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


def add_daily_timesheet(request):
    if request.method == 'POST':
        form = DailyTimesheetForm(request.POST)
        if form.is_valid():
                instance = form.save(commit=False)
                # instance.rate_day = instance.rate * instance.daily_prod_quant  # общее количество выработки одного сотрудника
                instance.save()
                return redirect('daily_timesheet2')
        else:
            form = DailyTimesheetForm()
    else:
        form = DailyTimesheetForm()

    return render(request, 'manufacture/new_daily_timesheet.html', {'form': form})


# поиск по Эва
# def search(request):
#     error = False
#     if 'q1' and 'q2' in request.GET:
#         q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
#         q2 = datetime.datetime.strptime(request.GET['q2'], '%Y-%m-%d')
#
#         if not q1:
#             error = True
#         elif not q2:
#             error = True
#         else:
#             quantities = DailyProduction.objects.filter(date__range=(q1, q2))
#             emp = Employee.objects.all()
#             return render(request, 'manufacture/raschet_pu.html',
#                           {'quantities': quantities,
#                            'q1': q1,
#                            'q2': q2,
#                            'emp': emp}
#                           )
#     return render(request, 'manufacture/search_form.html', {'error': error})


# отображение ежедневного табеля
def view_daily_timesheet(request):
    error = False
    if 'q1' in request.GET:
        q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
        if not q1:
            error = True
        else:
            timesheet = DailyTimesheet.objects.filter(date=q1)
            total_emp = DailyTimesheet.objects.filter(date=q1).count()
            total_prod = DailyTimesheet.objects.filter(date=q1).aggregate(TOTAL=Sum('daily_prod_quant'))['TOTAL']
            context = {
                'timesheet': timesheet,
                'q1': q1,
                'total_emp': total_emp,
                'total_prod': total_prod,
            }
            return render(request, 'manufacture/daily_timesheet2.html', context)

    return render(request, 'manufacture/daily_timesheet2.html', {'error': error})


def view_monthly_production(request):
    error = False
    if 'q1' and 'q2' in request.GET:
        q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
        q2 = datetime.datetime.strptime(request.GET['q2'], '%Y-%m-%d')

        if not q1:
            error = True
        elif not q2:
            error = True
        else:
            productions = DailyProduction.objects.filter(date__range=(q1, q2)).aggregate(TOTAL=Sum('quantity'))['TOTAL']
            products = Catalogue.objects.all()
            # col_model = Catalogue.objects.filter(model='model').count()
            return render(request, 'manufacture/monthly_productions.html',
                          {'productions': productions,
                           'q1': q1,
                           'q2': q2,
                           'products': products, }
                          # 'col_model': col_model}
                          )
    return render(request, 'manufacture/monthly_productions.html', {'error': error})


# catalogs = Catalogue.objects.all().values('model', 'code')
# dct = {}
# for catalog in catalogs:
#     if catalog['model'] not in dct:
#         dct[catalog['model']] = 1
#     else:
#         dct[catalog['model']] += 1
#
# print(dct, catalogs)


# col_model = Catalogue.objects.filter(model='Бенто').count()
# print(col_model)


# поиск по месячной выработке
def search_monthly(request):
    error = False
    if 'q1' and 'q2' in request.GET:
        q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
        q2 = datetime.datetime.strptime(request.GET['q2'], '%Y-%m-%d')

        if not q1:
            error = True
        elif not q2:
            error = True
        else:
            quantities = (DailyProduction.objects
                          .filter(date__range=(q1, q2))
                          .values('catalogue__color',
                                  'catalogue__code',
                                  'catalogue__model',
                                  'date',
                                  'quantity')
                          .annotate(total=Sum('quantity')).order_by('date'))

            total = (DailyProduction.objects
                     .values('date')
                     .filter(date__range=(q1, q2)).annotate(total=Sum('quantity')).order_by('date'))
            total_range = DailyProduction.objects.filter(date__range=(q1, q2)).order_by('date').aggregate(total=Sum('quantity'))['total']
            return render(request, 'manufacture/monthly_production2.html',
                          {'quantities': quantities,
                           'q1': q1,
                           'q2': q2,
                           'total': total,
                           'total_range': total_range,
                           }
                          )
    return render(request, 'manufacture/search_month.html', {'error': error})


def pandas_view(request):
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
            # df = read_frame(item)
            # df = read_frame(item, fieldnames=['date', 'quantity', 'catalogue', 'package', 'defect_worker'])
            rows = ['date']
            cols = ['catalogue']

            pt = item.to_pivot_table(values='quantity', rows=rows, cols=cols, aggfunc=np.sum, fill_value=0, margins=True)
            mydict = {
                "df": pt.to_html(),
                    }
            return render(request, 'manufacture/pandas_report.html', mydict)
    return render(request, 'manufacture/search_month.html', {'error': error})

# рассчет по ПУ
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

            pt = quantities.to_pivot_table(values=['daily_prod_quant', 'rate_day'], rows=rows, cols=cols, aggfunc=np.sum, fill_value=0, margins=True)
            mydict = {
                "df": pt.to_html(),
                    }
            return render(request, 'manufacture/raschet_pu.html', mydict)
    return render(request, 'manufacture/search_form.html', {'error': error})

# поиск по станку ЭВА
def search_eva(request):
    error = False
    if 'q1' and 'q2' in request.GET:
        q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')
        q2 = datetime.datetime.strptime(request.GET['q2'], '%Y-%m-%d')

        if not q1:
            error = True
        elif not q2:
            error = True
        else:
            quantities = DailyTimesheet.objects.filter(date__range=(q1, q2), stanok='ЭВА')
            rows = ['employee', 'rate']
            cols = ['date']

            pt = quantities.to_pivot_table(values=['daily_prod_quant', 'rate_day'], rows=rows, cols=cols, aggfunc=np.sum, fill_value=0, margins=True)
            mydict = {
                "df": pt.to_html(),
                    }
            return render(request, 'manufacture/raschet_eva.html', mydict)
    return render(request, 'manufacture/search_form_eva.html', {'error': error})



# общая зарплата
def salary_total1(request):
    salary_t = SalaryTotal.objects.all().order_by('-pk')
    return render(request, 'manufacture/salary_total1.html', {'salary_t': salary_t})