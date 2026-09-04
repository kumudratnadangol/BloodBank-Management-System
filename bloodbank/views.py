
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from .models import Donor, BloodBank, Hospital, BloodUnit, BloodRequest, RequestFulfillment
from .serializers import (
    DonorSerializer, BloodBankSerializer, HospitalSerializer,
    BloodUnitSerializer, BloodRequestSerializer, RequestFulfillmentSerializer
)
from .services import (
    DonorService, BloodBankService, HospitalService,
    BloodUnitService, BloodRequestService, RequestFulfillmentService, ReportService
)


class DonorListView(APIView):
    def get(self, request):
        donors = DonorService.get_all()
        serializer = DonorSerializer(donors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            donor = DonorService.create(serializer.validated_data)
            return Response(DonorSerializer(donor).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonorDetailView(APIView):
    def get(self, request, pk):
        donor = DonorService.get_by_id(pk)
        if not donor:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(DonorSerializer(donor).data)

    def put(self, request, pk):
        donor = DonorService.get_by_id(pk)
        if not donor:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DonorSerializer(donor, data=request.data, partial=True)
        if serializer.is_valid():
            updated = DonorService.update(pk, serializer.validated_data)
            return Response(DonorSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        donor = DonorService.get_by_id(pk)
        if not donor:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        DonorService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DonorBloodUnitsView(APIView):
    """Navigational query 1: GET /api/donors/<pk>/blood-units/"""
    def get(self, request, pk):
        units = DonorService.get_blood_units_by_donor(pk)
        return Response(BloodUnitSerializer(units, many=True).data)


class BloodBankListView(APIView):
    def get(self, request):
        banks = BloodBankService.get_all()
        return Response(BloodBankSerializer(banks, many=True).data)

    def post(self, request):
        serializer = BloodBankSerializer(data=request.data)
        if serializer.is_valid():
            bank = BloodBankService.create(serializer.validated_data)
            return Response(BloodBankSerializer(bank).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BloodBankDetailView(APIView):
    def get(self, request, pk):
        bank = BloodBankService.get_by_id(pk)
        if not bank:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BloodBankSerializer(bank).data)

    def put(self, request, pk):
        bank = BloodBankService.get_by_id(pk)
        if not bank:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BloodBankSerializer(bank, data=request.data, partial=True)
        if serializer.is_valid():
            updated = BloodBankService.update(pk, serializer.validated_data)
            return Response(BloodBankSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bank = BloodBankService.get_by_id(pk)
        if not bank:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        BloodBankService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BloodBankUnitsView(APIView):
    """Navigational query 2: GET /api/banks/<pk>/units/"""
    def get(self, request, pk):
        units = BloodBankService.get_units_by_bank(pk)
        return Response(BloodUnitSerializer(units, many=True).data)


class HospitalListView(APIView):
    def get(self, request):
        hospitals = HospitalService.get_all()
        return Response(HospitalSerializer(hospitals, many=True).data)

    def post(self, request):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            hospital = HospitalService.create(serializer.validated_data)
            return Response(HospitalSerializer(hospital).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HospitalDetailView(APIView):
    def get(self, request, pk):
        hospital = HospitalService.get_by_id(pk)
        if not hospital:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(HospitalSerializer(hospital).data)

    def put(self, request, pk):
        hospital = HospitalService.get_by_id(pk)
        if not hospital:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = HospitalSerializer(hospital, data=request.data, partial=True)
        if serializer.is_valid():
            updated = HospitalService.update(pk, serializer.validated_data)
            return Response(HospitalSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        hospital = HospitalService.get_by_id(pk)
        if not hospital:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        HospitalService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class HospitalRequestsView(APIView):
    """Navigational query 3: GET /api/hospitals/<pk>/requests/"""
    def get(self, request, pk):
        requests_qs = HospitalService.get_requests_by_hospital(pk)
        return Response(BloodRequestSerializer(requests_qs, many=True).data)

class BloodUnitListView(APIView):
    def get(self, request):
        units = BloodUnitService.get_all()
        return Response(BloodUnitSerializer(units, many=True).data)

    def post(self, request):
        serializer = BloodUnitSerializer(data=request.data)
        if serializer.is_valid():
            unit = BloodUnitService.create(serializer.validated_data)
            return Response(BloodUnitSerializer(unit).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BloodUnitDetailView(APIView):
    def get(self, request, pk):
        unit = BloodUnitService.get_by_id(pk)
        if not unit:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BloodUnitSerializer(unit).data)

    def put(self, request, pk):
        unit = BloodUnitService.get_by_id(pk)
        if not unit:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BloodUnitSerializer(unit, data=request.data, partial=True)
        if serializer.is_valid():
            updated = BloodUnitService.update(pk, serializer.validated_data)
            return Response(BloodUnitSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        unit = BloodUnitService.get_by_id(pk)
        if not unit:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        BloodUnitService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BloodRequestListView(APIView):
    def get(self, request):
        requests_qs = BloodRequestService.get_all()
        return Response(BloodRequestSerializer(requests_qs, many=True).data)

    def post(self, request):
        serializer = BloodRequestSerializer(data=request.data)
        if serializer.is_valid():
            req = BloodRequestService.create(serializer.validated_data)
            return Response(BloodRequestSerializer(req).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BloodRequestDetailView(APIView):
    def get(self, request, pk):
        req = BloodRequestService.get_by_id(pk)
        if not req:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BloodRequestSerializer(req).data)

    def put(self, request, pk):
        req = BloodRequestService.get_by_id(pk)
        if not req:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BloodRequestSerializer(req, data=request.data, partial=True)
        if serializer.is_valid():
            updated = BloodRequestService.update(pk, serializer.validated_data)
            return Response(BloodRequestSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        req = BloodRequestService.get_by_id(pk)
        if not req:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        BloodRequestService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestFulfillmentListView(APIView):
    def get(self, request):
        fulfillments = RequestFulfillmentService.get_all()
        return Response(RequestFulfillmentSerializer(fulfillments, many=True).data)

    def post(self, request):
        serializer = RequestFulfillmentSerializer(data=request.data)
        if serializer.is_valid():
            fulfillment = RequestFulfillmentService.create(serializer.validated_data)
            return Response(RequestFulfillmentSerializer(fulfillment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestFulfillmentDetailView(APIView):
    def get(self, request, pk):
        fulfillment = RequestFulfillmentService.get_by_id(pk)
        if not fulfillment:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(RequestFulfillmentSerializer(fulfillment).data)

    def delete(self, request, pk):
        fulfillment = RequestFulfillmentService.get_by_id(pk)
        if not fulfillment:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        RequestFulfillmentService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DonorHospitalTraceView(APIView):
    """Complex query 1: GET /api/reports/hospital/<pk>/trace/"""
    def get(self, request, pk):
        data = ReportService.get_donor_hospital_trace(pk)
        return Response(data)


class BankInventorySummaryView(APIView):
    """Complex query 2: GET /api/reports/bank-inventory/"""
    def get(self, request):
        data = ReportService.get_bank_inventory_summary()
        return Response(data)


class ExpireUnitsView(APIView):
    """
    Background task trigger: POST /api/tasks/expire-units/
    Client calls this to kick off the async job that marks expired blood units.
    """
def post(self, request):
        from .tasks import run_expire_units_task
        run_expire_units_task.delay() if hasattr(run_expire_units_task, 'delay') else run_expire_units_task()
        return Response({'message': 'Expiry check task triggered.'}, status=status.HTTP_202_ACCEPTED)


from django.shortcuts import render
from .models import Donor


def donors_page(request):
    donors = Donor.objects.all().order_by('donor_id')

    return render(request, 'donors.html', {
        'donors': donors
    })
def add_donor(request):

    if request.method == 'POST':

        Donor.objects.create(
            name=request.POST.get('name'),
            blood_group=request.POST.get('blood_group'),
            dob=request.POST.get('dob'),
            contact=request.POST.get('contact'),
            address=request.POST.get('address'),
            last_donation_date=request.POST.get('last_donation_date') or None
        )

        return redirect('donors_page')

    return render(request, 'add_donor.html')
def banks_page(request):
    return render(request, 'banks.html')
def hospitals_page(request):
    return render(request, 'hospitals.html')
def blood_units_page(request):
    return render(request, 'blood_units.html')
def requests_page(request):
    return render(request, 'requests.html')
def reports_page(request):
    return render(request, 'reports.html')