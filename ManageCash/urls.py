from django.contrib import admin
from django.urls import path
from ManageCash.views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', login_page, name='logout'),
    path('addExpense/', add_expense_view, name='addExpense'),
    path('addCash/', add_cash_view, name='addCash'),
]
