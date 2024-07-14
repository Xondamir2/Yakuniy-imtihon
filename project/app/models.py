from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    name = models.CharField(max_length=255, help_text='введите девайс')
    image = models.ImageField(upload_to='device_image/', help_text='картинка девайса')

class ExpensesCategory(models.Model):
    name = models.CharField(max_length=255, help_text='Категории Расходов')
    image = models.ImageField(upload_to='expenses_image/', help_text='Картинка категории расходов')

    def __str__(self):
        return self.name

class IncomeCategory(models.Model):
    name = models.CharField(max_length=255, help_text='Категории Доходов')
    image = models.ImageField(upload_to='income_image/', help_text='Картинка категории доходов')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', '-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text='сколько денег вы хотите добавить')
    picture = models.ImageField(upload_to='profile/', blank=True, null=True, help_text='картинка пользователя * необезательно')
    date_of_birth = models.DateField(help_text='Дата рождения')
    address = models.CharField(max_length=255, blank=True, null=True, help_text='Адрес * необезательно')
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text='Номер телефона * необезательно')
    bio = models.TextField(help_text='О мне')
    gender = models.CharField(max_length=1, choices=CHOICES, help_text='Пол')

    def __str__(self):
        return self.user.username


class Expenses(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, help_text='введите девайс которым пользуетесь')
    category = models.ForeignKey(ExpensesCategory, on_delete=models.CASCADE)
    description = models.TextField(help_text='Описание расходов', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_wallet_balance(self.user, -self.amount)

class Income(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, help_text='введите девайс которым пользуетесь')
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    description = models.TextField(help_text='Описание доходов', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_wallet_balance(self.user, self.amount)

def update_wallet_balance(user, amount):
    profile = user.userprofile
    profile.wallet_balance += amount
    profile.save()


