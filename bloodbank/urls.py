
from django.urls import path
from . import views

urlpatterns = [
    # Donor
    path('donors/', views.DonorListView.as_view()),
    path('donors/<int:pk>/', views.DonorDetailView.as_view()),
    path('donors/<int:pk>/blood-units/', views.DonorBloodUnitsView.as_view()),

    # BloodBank
    path('banks/', views.BloodBankListView.as_view()),
    path('banks/<int:pk>/', views.BloodBankDetailView.as_view()),
    path('banks/<int:pk>/units/', views.BloodBankUnitsView.as_view()),

    # Hospital
    path('hospitals/', views.HospitalListView.as_view()),
    path('hospitals/<int:pk>/', views.HospitalDetailView.as_view()),
    path('hospitals/<int:pk>/requests/', views.HospitalRequestsView.as_view()),

    # BloodUnit
    path('units/', views.BloodUnitListView.as_view()),
    path('units/<int:pk>/', views.BloodUnitDetailView.as_view()),

    # BloodRequest
    path('requests/', views.BloodRequestListView.as_view()),
    path('requests/<int:pk>/', views.BloodRequestDetailView.as_view()),

    # RequestFulfillment
    path('fulfillments/', views.RequestFulfillmentListView.as_view()),
    path('fulfillments/<int:pk>/', views.RequestFulfillmentDetailView.as_view()),

    # Complex queries (reports)
    path('reports/hospital/<int:pk>/trace/', views.DonorHospitalTraceView.as_view()),
    path('reports/bank-inventory/', views.BankInventorySummaryView.as_view()),

    # Background task trigger
    path('tasks/expire-units/', views.ExpireUnitsView.as_view()),
]