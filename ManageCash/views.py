from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, AddCashForm, ExpenseForm

from django.contrib.auth.decorators import login_required
from operator import attrgetter

from itertools import chain

from .models import AddCash, Expense

# Create your views here.
def register_page(request):
    if request.method =='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successfull! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm
    return render(request, 'register.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = None

        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                username_or_email = user_obj.username
            except User.DoesNotExist:
                pass

        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username/password.')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def profile_view(request):
    return render(request, 'profile.html')



@login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    income_records = AddCash.objects.filter(user=request.user)
    expense_records = Expense.objects.filter(user=request.user)
    
    total_income = sum(item.amount for item in income_records)
    total_expense = sum(item.amount for item in expense_records)
    remaining_balance = total_income - total_expense
    
    all_transactions = sorted(
        chain(income_records, expense_records),
        key=attrgetter('datetime'),
        reverse=True
    )
    
    context = {
        'remaining_balance': remaining_balance,
        'transactions': all_transactions,
    }
    
    return render(request, 'home.html', context)


@login_required(login_url='login')
def add_cash_view(request):
    if request.method == 'POST':
        form = AddCashForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('home')
    else:
        form = AddCashForm()
    return render(request, 'addCash.html', {'form': form})

@login_required(login_url='login')
def add_expense_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'addExpense.html', {'form': form})