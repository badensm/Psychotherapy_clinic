from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/<int:user_id>', views.account, name='account'),
    path('visit/list', views.visit_list, name='visit_list'),
    path('visit/detail/<int:visit_id>', views.visit_detail, name='visit_detail'),
    path('visit/create_patient/<int:user_id>/<int:therapist_id>' ,views.create_visit_patient, name='create_visit_patient'),
    path('visit/create_therapist/<int:user_id>' ,views.create_visit_therapist, name='create_visit_therapist'),
    path('visit/cancel/<int:visit_id>', views.cancel_visit, name='cancel_visit'),
    path('visit/create/user/<int:user_id>',views.visit_create_user, name='visit_create_user'),
    path('visit/create/choose_therapist/<int:user_id>',views.choose_therapist, name='choose_therapist'),
    path('visit/create/patient/<int:user_id>/<int:therapist_id>', views.visit_create_patient, name='visit_create_patient'),
    path('visit/create/therapist/<int:user_id>', views.visit_create_therapist, name='visit_create_therapist'),
    path('visit/confirm_visit/<int:visit_id>', views.confirm_visit, name='confirm_visit'),
    path('visit/reserve/therapist/<int:user_id>', views.visit_reserve_therapist, name='visit_reserve_therapist'),
    path('therapist/schedule', views.therapist_schedule, name='therapist_schedule'),
    path('therapist/reserved/cancel/<int:user_id>', views.cancel_reserved, name='cancel_reserved'),
    path('patient/edit/symptoms/<int:user_id>', views.patient_symptoms_edit, name='patient_symptoms_edit'),
    path('therapist/edit/data/<int:user_id>', views.therapist_data_edit, name='therapist_data_edit'),
    path('therapist/edit/patient/<int:patient_id>', views.therapist_patient_edit, name='therapist_patient_edit'),
    path('therapist/patient_list', views.patient_list, name='patient_list'),
    path('therapist_list', views.therapist_list, name='therapist_list'),
]
