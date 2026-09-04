
from rest_framework import serializers
from .models import Donor, BloodBank, Hospital, BloodUnit, BloodRequest, RequestFulfillment


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'


class BloodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBank
        fields = '__all__'


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'


class BloodUnitSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(source='donor.name', read_only=True)
    bank_name = serializers.CharField(source='bank.name', read_only=True)

    class Meta:
        model = BloodUnit
        fields = '__all__'


class BloodRequestSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)

    class Meta:
        model = BloodRequest
        fields = '__all__'


class RequestFulfillmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestFulfillment
        fields = '__all__'