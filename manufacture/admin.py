from django.contrib import admin
from .models import *


class DailyProductionAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'catalogue',
        'quantity',
        'package',
        'defect_worker',
        'defect_machine',
        'defect_saya',
        'show_sum'
    )
    list_filter = ('date',)

    def show_sum(self, obj):
        from django.db.models import Sum
        result = DailyProduction.objects.filter(date=obj.date).aggregate(TOTAL=Sum("quantity"))['TOTAL']
        return result


admin.site.register(Sale)
admin.site.register(SalaryTotal)
admin.site.register(Employee)
admin.site.register(DailyProduction, DailyProductionAdmin)
admin.site.register(Catalogue)
admin.site.register(DailyTimesheet)
admin.site.register(Client)
