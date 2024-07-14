from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ExpensesCategory, IncomeCategory, UserProfile, Expenses, Income



class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))



class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parol'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parolni takrorlang'
    }))

    class Meta:
        model = User
        fields = ('username', 'email')


class ExpensesCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpensesCategory
        fields = ['name', 'image']


class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['name', 'image']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'user', 'wallet_balance', 'picture', 'date_of_birth',
            'address', 'phone_number', 'bio', 'gender']


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['amount', 'date', 'category', 'description', 'user']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'category', 'description', 'user']

