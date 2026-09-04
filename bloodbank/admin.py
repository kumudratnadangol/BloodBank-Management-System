from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Donor, BloodBank, Hospital, BloodUnit, BloodRequest, RequestFulfillment


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('donor_id', 'name', 'blood_group', 'contact', 'last_donation_date')
    search_fields = ('name', 'blood_group')


@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ('bank_id', 'name', 'location', 'contact')


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('hospital_id', 'name', 'location', 'contact')


@admin.register(BloodUnit)
class BloodUnitAdmin(admin.ModelAdmin):
    list_display = ('unit_id', 'donor', 'bank', 'blood_group', 'status', 'expiry_date')
    list_filter = ('status', 'blood_group')


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'hospital', 'blood_group', 'units_requested', 'status', 'request_date')
    list_filter = ('status', 'blood_group')


@admin.register(RequestFulfillment)
class RequestFulfillmentAdmin(admin.ModelAdmin):
    list_display = ('fulfillment_id', 'request', 'unit', 'fulfilled_date')