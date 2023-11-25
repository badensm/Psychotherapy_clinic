from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('visit_list', views.visit_list, name='visit_list')
]
