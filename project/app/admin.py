from django.contrib import admin
from .models import ExpensesCategory, IncomeCategory, Expenses, Income, UserProfile, Device
# Register your models here.


admin.site.register(ExpensesCategory)
admin.site.register(IncomeCategory)
admin.site.register(Expenses)
admin.site.register(Income)
admin.site.register(UserProfile)
admin.site.register(Device)