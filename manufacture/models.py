from django.db import models
from django.db.models import Sum


class Sale(models.Model):
    date = models.DateField()
    client = models.ForeignKey('Client', on_delete=models.PROTECT, verbose_name='Клиент', blank=True)
    model = models.ForeignKey('Catalogue', on_delete=models.CASCADE, verbose_name='Mодель')
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
        return f'{self.client}, {self.model}'


class Catalogue(models.Model):
    model = models.CharField(max_length=100, verbose_name='Модель')  # Артикул модели
    image = models.ImageField(upload_to='media/products/%Y/%m/%d', blank=True, verbose_name="Фото")  # Фото товара
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Код")  # Название модели
    color = models.CharField(max_length=100, verbose_name="Цвет")  # Тип модели обуви(цвета, отделка, и т.д.)
    size = models.CharField(max_length=100, verbose_name="Размеры")  # Размерная сетка

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return f'{self.model}, {self.code}, {self.color}'


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
    occupation = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    date_start = models.DateField(verbose_name="Дата начала работы", blank=True)
    fio = models.CharField(max_length=64, unique=True, verbose_name="ФИО")  # имя фамилия отчество сотрудника
    phone = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")
    phone1 = models.CharField(max_length=20, blank=True, verbose_name="Дополнительный номер")
    monthly_salary = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f'{self.fio}'


class Client(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, verbose_name='Клиент')
    phone = models.CharField(max_length=100, verbose_name='Номер телефона')
    address = models.CharField(max_length=100, blank=True, verbose_name='Адрес клиента')
    file = models.FileField(upload_to='media/clients/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'{self.name}, {self.phone}'


class DailyTimesheet(models.Model):
    date = models.DateField()
    employee = models.ForeignKey('Employee', on_delete=models.RESTRICT, )
    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'employee'], name="unique_date_for_employee"
            ),
        ]

    def __str__(self):
        return f'{self.date}'

    @property
    def emp_sum(self):
        if self.id:
            return DailyTimesheet.objects.aggregate(TOTAL=Sum('employee'))['TOTAL']
        return DailyTimesheet.objects.none()

    @property
    def emp_count(self):
        if self.date:
            return DailyTimesheet.objects.filter(date=self.date).count()
        return DailyTimesheet.objects.none()


class DailyProduction(models.Model):
    date = models.DateField()
    catalogue = models.ForeignKey('Catalogue', on_delete=models.CASCADE, related_name='catalogues',
                                  verbose_name="Модель")
    quantity: int = models.IntegerField(default=0, verbose_name="Кол. пар")
    package: int = models.IntegerField(blank=True, verbose_name='Упаковка')
    defect_worker = models.PositiveIntegerField(default=0, verbose_name="Брак рабочие")
    defect_machine = models.PositiveIntegerField(default=0, verbose_name="Брак станок")
    defect_saya = models.PositiveIntegerField(default=0, verbose_name="Брак САЯ")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', )
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def fetch_package(self):
        self.package = self.quantity // 6
        return self.package

    def __str__(self):
        return f'{self.date}, {self.catalogue}'

    def defect_q(self):
        return self.defect_machine + self.defect_worker + self.defect_saya  # общее количество бракa

    def defect_sum(self):
        return (self.defect_machine + self.defect_worker + self.defect_saya) * 200  # брак по 200 сом за 1 брак


