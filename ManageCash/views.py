from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import AddCash, Expense
from django.contrib.auth.decorators import login_required

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
    return render(request, 'registration.html', {'form': form})

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
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username/password.')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    add_cash_records = AddCash.objects.filter(user=request.user)
    expense_records = Expense.objects.filter(user=request.user)
    context = {
        'add_cash_records': add_cash_records,
        'expense_records': expense_records,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'profile.html')

@login_required(login_url='login')
def add_transaction_view(request):
    if request.method == 'POST':
        trans_type = request.POST.get('trans_type')
        if trans_type == 'income':
            form = AddCashForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return redirect('dashboard')
        elif trans_type == 'expense':
            form = ExpenseForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return redirect('dashboard')
    else:
        income_form = AddCashForm()
        expense_form = ExpenseForm()
    return render(request, 'transaction_form.html', {'income_form': income_form, 'expense_form': expense_form})