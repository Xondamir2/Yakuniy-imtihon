from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, RegisterForm, ExpensesCategoryForm, IncomeCategoryForm, UserProfileForm, ExpensesForm, IncomeForm
from .models import Expenses, Income, ExpensesCategory, IncomeCategory
import random
from .models import UserProfile
from django.shortcuts import redirect
from django.contrib.auth.models import User
# Create your views here.
def generate_color(category=None):
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def index(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    total_wallet_amount = user_profile.wallet_balance
    expenses_categories = ExpensesCategory.objects.all()
    income_categories = IncomeCategory.objects.all()
    expenses = Expenses.objects.filter(user=user)
    income = Income.objects.filter(user=user)
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    total_income = income.aggregate(total=Sum('amount'))['total'] or 0
    expenses_percentage = calculate_percentage(expenses, 'expense')
    income_percentage = calculate_percentage(income, 'income')

    context = {
        'total_wallet_amount': total_wallet_amount,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'expenses_percentage': expenses_percentage,
        'income_percentage': income_percentage,
        'expenses_categories': expenses_categories,
        'income_categories': income_categories,
    }

    return render(request, 'app/index.html', context)

def calculate_percentage(transactions, transaction_type):
    total_amount = transactions.aggregate(total=Sum('amount'))['total'] or 0
    percentages = []
    if transaction_type == 'expense':
        categories = ExpensesCategory.objects.all()
    elif transaction_type == 'income':
        categories = IncomeCategory.objects.all()
    else:
        return percentages

    for category in categories:
        category_amount = transactions.filter(category=category).aggregate(total=Sum('amount'))['total'] or 0
        percentage = (category_amount / total_amount * 100) if total_amount > 0 else 0
        color = generate_color()
        percentages.append({
            'category': category.name,
            'percentage': percentage,
            'color': color
        })

    return percentages



def create_expenses_category(request):
    if request.method == 'POST':
        form = ExpensesCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses_category')
    else:
        form = ExpensesCategoryForm()
    return render(request, 'app/create_expenses_category.html', {'form': form})

def create_income_category(request):
    if request.method == 'POST':
        form = IncomeCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_category')
    else:
        form = IncomeCategoryForm()
    return render(request, 'app/create_income_category.html', {'form': form})

def create_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm()
    return render(request, 'app/create_user_profile.html', {'form': form})

def create_expenses(request):
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        form = ExpensesForm()
    return render(request, 'app/create_expenses.html', {'form': form})

def create_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income')
    else:
        form = IncomeForm()
    return render(request, 'app/create_income.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    return render(request, 'app/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def user_register(request):
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('index')
    form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'app/register.html', context)
