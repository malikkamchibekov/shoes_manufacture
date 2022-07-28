from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime
from django_tables2 import SingleTableView, tables, RequestConfig
from django.db.models import Sum, Count
import datetime

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
                return redirect('salary_total')
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
                employer = form.save()
                employer.save()
                return redirect('employer')
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
    production = DailyProduction.objects.all()
    total_quantity = DailyProduction.objects.aggregate(TOTAL=Sum('quantity'))['TOTAL']
    total_defect_worker = DailyProduction.objects.aggregate(TOTAL=Sum('defect_worker'))['TOTAL']
    total_defect_machine = DailyProduction.objects.aggregate(TOTAL=Sum('defect_machine'))['TOTAL']
    total_defect_saya = DailyProduction.objects.aggregate(TOTAL=Sum('defect_saya'))['TOTAL']

    context = {
        'production': production,
        'total_quantity': total_quantity,
        'total_defect_worker': total_defect_worker,
        'total_defect_machine': total_defect_machine,
        'total_defect_saya': total_defect_saya,
    }
    return render(request, 'manufacture/daily_production.html', context)


# добавление ежедневки
def add_daily_production(request):
    if request.method == 'POST':
        form = DailyProductionForm(request.POST)
        if form.is_valid():
            try:
                daily_production = form.save()
                daily_production.fetch_package()
                daily_production.save()
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
            try:
                daily_timesheet = form.save()
                daily_timesheet.save()
                return redirect('daily_timesheet')
            except:
                form.add_error(None, "Что-то пошло не так, попробуйте снова")
        else:
            form = DailyTimesheetForm()
    else:
        form = DailyTimesheetForm()
    return render(request, 'manufacture/new_daily_timesheet.html', {'form': form})


# отображение ежедневного табеля
def view_daily_timesheet(request):
    timesheet = DailyTimesheet.objects.all().order_by('-pk')
    return render(request, 'manufacture/daily_timesheet.html', {'timesheet': timesheet})

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
            quantities = DailyProduction.objects.filter(date__range=(q1,q2))
            emp = Employee.objects.all()
            return render(request, 'manufacture/raschet_pu.html',
                {'quantities': quantities,
                 'q1': q1,
                 'q2': q2,
                 'emp': emp }
                )
    return render(request, 'manufacture/search_form.html', {'error': error})



# отображение ежедневного табеля II version
def view_daily_timesheet2(request):
    error = False
    if 'q1'  in request.GET:
        q1 = datetime.datetime.strptime(request.GET['q1'], '%Y-%m-%d')

        if not q1:
            error = True
        else:
            timesheet = DailyTimesheet.objects.filter(date='2022-07-01')
            total_emp = DailyTimesheet.objects.filter(date='2022-07-01').count()
            return render(request, 'manufacture/daily_timesheet2.html',{'timesheet': timesheet,'q1': q1, 'total_emp': total_emp })

    return render(request, 'manufacture/daily_timesheet2.html', {'error': error})


