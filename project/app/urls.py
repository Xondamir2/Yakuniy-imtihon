from django.urls import path
from . import views
from .views import user_register, user_login, user_logout



urlpatterns = [
    path('', views.index, name='index'),
    path('expenses_category_create/', views.create_expenses_category, name='expenses_category'),
    path('income_category_create/', views.create_income_category, name='income_category'),
    path('user_profile_create/', views.create_user_profile, name='user_profile'),
    path('expenses_create/', views.create_expenses, name='expenses'),
    path('income_create/', views.create_income, name='income'),
    path('register/', user_register, name="register"),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
