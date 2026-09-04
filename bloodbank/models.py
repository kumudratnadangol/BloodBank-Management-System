
from django.db import models


class Donor(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    donor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    dob = models.DateField()
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)
    last_donation_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'DONOR'

    def __str__(self):
        return f"{self.name} ({self.blood_group})"


class BloodBank(models.Model):
    bank_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)

    class Meta:
        db_table = 'BLOOD_BANK'

    def __str__(self):
        return self.name


class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)

    class Meta:
        db_table = 'HOSPITAL'

    def __str__(self):
        return self.name


class BloodUnit(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Expired', 'Expired'),
        ('Used', 'Used'),
    ]

    unit_id = models.AutoField(primary_key=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='blood_units')
    bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='blood_units')
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUP_CHOICES)
    collection_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')

    class Meta:
        db_table = 'BLOOD_UNIT'

    def __str__(self):
        return f"Unit {self.unit_id} - {self.blood_group} ({self.status})"


class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Fulfilled', 'Fulfilled'),
    ]

    request_id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='requests')
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUP_CHOICES)
    units_requested = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    request_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'BLOOD_REQUEST'

    def __str__(self):
        return f"Request {self.request_id} - {self.hospital.name} ({self.status})"


class RequestFulfillment(models.Model):
    fulfillment_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='fulfillments')
    unit = models.ForeignKey(BloodUnit, on_delete=models.CASCADE, related_name='fulfillments')
    fulfilled_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'REQUEST_FULFILLMENT'

    def __str__(self):
        return f"Fulfillment {self.fulfillment_id} - Request {self.request_id}"