from django.urls import path
from .views import *
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', home, name='home'),
    path('sales', sale_total, name='sales'),
    path('new_sale', add_new_sale, name='new_sale'),
    path('emp_report', employers, name='employers'),
    path('new_employer', add_employer, name='new_employer'),
    path('edit_sale/<int:id>', edit_sale, name='edit_sale'),
    path('delete_sale/<int:id>', delete_sale, name='delete_sale'),
    path('new_client', add_new_client, name='new_client'),
    path('clients', view_client, name='clients'),
    path('catalogue', view_catalogue, name='catalogue'),
    path('new_product', add_new_product, name='new_product'),
    path('daily_production', view_daily_production, name='daily_production'),
    path('new_daily_production', add_daily_production, name='new_daily_production'),
    path('new_daily_timesheet', add_daily_timesheet, name='new_daily_timesheet'),
    path('search_form', search_pu, name='search_form'),
    path('search_form_eva', search_eva, name='search_form_eva'),
    path('daily_timesheet2', view_daily_timesheet, name='daily_timesheet2'),
    path('search_month', search_monthly, name='search_month'),
    path('monthly_production2', search_monthly, name='monthly_production2'),
    path('pandas_report', pandas_view, name='pandas_report'),
    path('salary_total1', salary_total1, name='salary_t'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('login/', user_login, name='login'),
    path('register_new/', register_new, name='register_new'),
]
