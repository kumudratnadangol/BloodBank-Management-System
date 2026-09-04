
from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone
from .models import Donor, BloodBank, Hospital, BloodUnit, BloodRequest, RequestFulfillment


class DonorService:
    @staticmethod
    def get_all():
        return Donor.objects.all()

    @staticmethod
    def get_by_id(donor_id):
        return Donor.objects.filter(donor_id=donor_id).first()

    @staticmethod
    def create(data):
        return Donor.objects.create(**data)

    @staticmethod
    def update(donor_id, data):
        Donor.objects.filter(donor_id=donor_id).update(**data)
        return DonorService.get_by_id(donor_id)

    @staticmethod
    def delete(donor_id):
        return Donor.objects.filter(donor_id=donor_id).delete()

    @staticmethod
    def get_blood_units_by_donor(donor_id):
        """Navigational query 1: all blood units donated by a given donor."""
        return BloodUnit.objects.filter(donor_id=donor_id)


class BloodBankService:
    @staticmethod
    def get_all():
        return BloodBank.objects.all()

    @staticmethod
    def get_by_id(bank_id):
        return BloodBank.objects.filter(bank_id=bank_id).first()

    @staticmethod
    def create(data):
        return BloodBank.objects.create(**data)

    @staticmethod
    def update(bank_id, data):
        BloodBank.objects.filter(bank_id=bank_id).update(**data)
        return BloodBankService.get_by_id(bank_id)

    @staticmethod
    def delete(bank_id):
        return BloodBank.objects.filter(bank_id=bank_id).delete()

    @staticmethod
    def get_units_by_bank(bank_id):
        """Navigational query 2: all blood units currently held by a given bank."""
        return BloodUnit.objects.filter(bank_id=bank_id)


class HospitalService:
    @staticmethod
    def get_all():
        return Hospital.objects.all()

    @staticmethod
    def get_by_id(hospital_id):
        return Hospital.objects.filter(hospital_id=hospital_id).first()

    @staticmethod
    def create(data):
        return Hospital.objects.create(**data)

    @staticmethod
    def update(hospital_id, data):
        Hospital.objects.filter(hospital_id=hospital_id).update(**data)
        return HospitalService.get_by_id(hospital_id)

    @staticmethod
    def delete(hospital_id):
        return Hospital.objects.filter(hospital_id=hospital_id).delete()

    @staticmethod
    def get_requests_by_hospital(hospital_id):
        """Navigational query 3: all requests made by a given hospital."""
        return BloodRequest.objects.filter(hospital_id=hospital_id)


class BloodUnitService:
    @staticmethod
    def get_all():
        return BloodUnit.objects.all()

    @staticmethod
    def get_by_id(unit_id):
        return BloodUnit.objects.filter(unit_id=unit_id).first()

    @staticmethod
    def create(data):
        return BloodUnit.objects.create(**data)

    @staticmethod
    def update(unit_id, data):
        BloodUnit.objects.filter(unit_id=unit_id).update(**data)
        return BloodUnitService.get_by_id(unit_id)

    @staticmethod
    def delete(unit_id):
        return BloodUnit.objects.filter(unit_id=unit_id).delete()


class BloodRequestService:
    @staticmethod
    def get_all():
        return BloodRequest.objects.all()

    @staticmethod
    def get_by_id(request_id):
        return BloodRequest.objects.filter(request_id=request_id).first()

    @staticmethod
    def create(data):
        return BloodRequest.objects.create(**data)

    @staticmethod
    def update(request_id, data):
        BloodRequest.objects.filter(request_id=request_id).update(**data)
        return BloodRequestService.get_by_id(request_id)

    @staticmethod
    def delete(request_id):
        return BloodRequest.objects.filter(request_id=request_id).delete()


class RequestFulfillmentService:
    @staticmethod
    def get_all():
        return RequestFulfillment.objects.all()

    @staticmethod
    def get_by_id(fulfillment_id):
        return RequestFulfillment.objects.filter(fulfillment_id=fulfillment_id).first()

    @staticmethod
    def create(data):
        """Creates a fulfillment record AND marks the linked BloodUnit as Used."""
        fulfillment = RequestFulfillment.objects.create(**data)
        unit = fulfillment.unit
        unit.status = 'Used'
        unit.save()
        return fulfillment

    @staticmethod
    def delete(fulfillment_id):
        return RequestFulfillment.objects.filter(fulfillment_id=fulfillment_id).delete()


class ReportService:
    """Houses the two complex, multi-entity queries."""

    @staticmethod
    def get_donor_hospital_trace(hospital_id):
        """
        Complex query 1 (3+ entities: Hospital -> BloodRequest -> RequestFulfillment
        -> BloodUnit -> Donor).
        For a given hospital, returns donor names and blood groups of all units
        that fulfilled its requests.
        """
        fulfillments = RequestFulfillment.objects.filter(
            request__hospital_id=hospital_id
        ).select_related('unit__donor', 'request')

        result = []
        for f in fulfillments:
            result.append({
                'request_id': f.request.request_id,
                'donor_name': f.unit.donor.name,
                'donor_blood_group': f.unit.donor.blood_group,
                'unit_id': f.unit.unit_id,
                'fulfilled_date': f.fulfilled_date,
            })
        return result

    @staticmethod
    def get_bank_inventory_summary():
        """
        Complex query 2 (3+ entities: BloodBank -> BloodUnit -> RequestFulfillment
        -> BloodRequest).
        For each blood bank, shows total units, available units, and how many
        units are already reserved for pending/approved requests.
        """
        banks = BloodBank.objects.annotate(
            total_units=Count('blood_units'),
            available_units=Count(
                'blood_units',
                filter=models.Q(blood_units__status='Available')
            ),
        )

        result = []
        for bank in banks:
            reserved_count = RequestFulfillment.objects.filter(
                unit__bank_id=bank.bank_id,
                request__status__in=['Pending', 'Approved']
            ).count()
            result.append({
                'bank_id': bank.bank_id,
                'bank_name': bank.name,
                'total_units': bank.total_units,
                'available_units': bank.available_units,
                'reserved_for_requests': reserved_count,
            })
        return result

    @staticmethod
    def expire_old_units():
        """
        Background task logic: scans all BloodUnit records and marks any
        past their expiry_date as 'Expired'.
        Returns the count of units updated.
        """
        today = timezone.now().date()
        updated_count = BloodUnit.objects.filter(
            expiry_date__lt=today
        ).exclude(status='Expired').update(status='Expired')
        return updated_count