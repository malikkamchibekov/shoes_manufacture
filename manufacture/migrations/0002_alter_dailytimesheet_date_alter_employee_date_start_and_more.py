# Generated by Django 4.0.6 on 2022-07-25 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacture', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytimesheet',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_start',
            field=models.DateField(blank=True, verbose_name='Дата начала работы'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='client',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='manufacture.client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=40, verbose_name='Сумма сом'),
        ),
    ]
