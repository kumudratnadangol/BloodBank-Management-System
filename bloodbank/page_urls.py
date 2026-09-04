from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('/donors/'), name='home'),
    path('donors/', views.donors_page, name='donors_page'),
    path('banks/', views.banks_page, name='banks_page'),
    path('hospitals/', views.hospitals_page, name='hospitals_page'),
    path('units/', views.blood_units_page, name='blood_units'),
    path('requests/', views.requests_page, name='requests'),
    path('reports/', views.reports_page, name='reports'),
    path('donors/add/', views.add_donor, name='add_donor'),
]