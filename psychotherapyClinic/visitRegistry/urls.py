from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/<int:user_id>/', views.account, name='account'),
    path('visit/list', views.visit_list, name='visit_list'),
    path('visit/detail/<int:visit_id>', views.visit_detail, name='visit_detail'),
    path('visit/confirm_visit/<int:visit_id>', views.confirm_visit, name='confirm_visit'),
    path('therapist/schedule/<int:therapist_id>', views.therapist_schedule, name='therapist_schedule')
]
