from django.db import models
from django.db.models import Sum

class Sale(models.Model):
    client = models.ForeignKey('Client', on_delete=models.PROTECT, verbose_name='Клиент', blank=True)
    vendor_code = models.CharField(max_length=40, verbose_name='Артикул')
    title = models.CharField(max_length=40, verbose_name="Наименование")
    type = models.CharField(max_length=40, verbose_name="Модель")
    size = models.CharField(max_length=40, verbose_name="Размер")
    quantity = models.IntegerField(default=0, verbose_name="Кол-во")
    price = models.DecimalField(max_digits=40, decimal_places=2, default=0, verbose_name="Цена сом")
    total = models.DecimalField(max_digits=40, decimal_places=2, verbose_name="Сумма сом")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def fetch_total(self):
        self.total = self.quantity * self.price
        return self.total

    def __str__(self):
        return f'{self.vendor_code}'


class Catalogue(models.Model):
    vendor_code = models.CharField(max_length=40, verbose_name='Артикул')  # Артикул модели
    image = models.ImageField(upload_to='media/products/%Y/%m/%d', blank=True, verbose_name="Фото")  # Фото товара
    title = models.CharField(max_length=40, blank=True, null=True, verbose_name="Наименование")  # Название модели
    type = models.CharField(max_length=40, verbose_name="Тип модели")  # Тип модели обуви(цвета, отделка, и т.д.)
    size = models.CharField(max_length=40, verbose_name="Размеры")  # Размерная сетка
    # rest_quantity = models.PositiveIntegerField()  # Остаток на складе

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return f'{self.vendor_code}'


class SalaryTotal(models.Model):  # общая зарплата
    employee = models.OneToOneField('Employee', on_delete=models.CASCADE, primary_key=True)
#    occupation = models.ForeignKey('Occupation', null=True, blank=True, on_delete=models.CASCADE,
                              #     related_name='salary_occupation')
    sales = models.ForeignKey('Sale', on_delete=models.CASCADE, null=True, blank=True, related_name='salary_sales')
    # working_out = models.OneToOneField('Production', on_delete=models.CASCADE, null=True, blank=True)
    month = models.DateTimeField(auto_now=True)
    working_days = models.IntegerField(null=True)
    fact_work_days = models.IntegerField(null=True)
    oklad_social_fund = models.IntegerField(null=True)
    oklad_fact = models.IntegerField(null=True)
    social_fund = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    firm_social_fund = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    oklad_nachislen = models.IntegerField(null=True)
    viplata = models.IntegerField(null=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.viplata}'


class Employee(models.Model):
    active = models.BooleanField(default=True)
    occupation = models.CharField(max_length=100, blank=True)
    date_start = models.DateField(verbose_name="Дата начала работы", blank=True)
    fio = models.CharField(max_length=64, unique=True)  # имя фамилия отчество сотрудника
    phone = models.CharField(max_length=20, blank=True)
    phone1 = models.CharField(max_length=20, blank=True)
    monthly_salary = models.IntegerField(default=0)


    def __str__(self):
        return self.fio


class Client(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, verbose_name='Клиент')
    phone = models.CharField(max_length=100, verbose_name='Номер телефона')
    address = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='media/clients/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'{self.name}, {self.phone}'


class DailyTimesheet(models.Model):
    date = models.DateField(verbose_name="Дата")
    employee = models.ForeignKey('Employee', on_delete=models.DO_NOTHING)
    objects = models.Manager()


    def __str__(self):
        return f'{self.date}'

    def __str__(self):
        return f'{self.employee}'

    @property
    def emp_sum(self):
        if self.id:
            return DailyTimesheet.objects.aggregate(TOTAL=Sum('employee'))['TOTAL']
        return DailyTimesheet.objects.none()

    @property
    def emp_count(self, d):
        if self.date:
            return DailyTimesheet.objects.filter(date=d).count()
        return DailyTimesheet.objects.none()

class DailyProduction(models.Model):
    timesheet = models.ForeignKey('DailyTimesheet', on_delete=models.CASCADE, verbose_name='Табель')
    catalogue = models.ForeignKey('Catalogue', on_delete=models.CASCADE, related_name='catalogues', verbose_name="Модель")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Кол. пар")
    package = models.PositiveIntegerField(blank=True)
    defect_worker = models.PositiveIntegerField(default=0, verbose_name="Брак рабочие")
    defect_machine = models.PositiveIntegerField(default=0, verbose_name="Брак станок")
    defect_saya = models.PositiveIntegerField(default=0, verbose_name="Брак САЯ")
    date = models.DateField(verbose_name="Дата", null=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', )
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')



    def fetch_package(self):
        return f'{self.quantity // 6}'

    def __str__(self):
        return f'{self.id}'

    def __str__(self):
        return f'{self.quantity}'

    def __str__(self):
        return f'{self.timesheet.date}'

    def sum_q(self):  # сумма выработанного количества по 5 сом
        return f'{self.quantity * 5}'

    def defect_q(self):
        return f'{self.defect_machine + self.defect_worker + self.defect_saya }' # общее количество брака

    def defect_sum(self):
        return f'{(self.defect_machine + self.defect_worker + self.defect_saya) * 200 }' # брак по 200 сом за 1 брак



