from datetime import datetime

from django.conf import settings
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Client(models.Model):

    POTENTIAL = "POTENTIAL"
    ACTUAL = "ACTUAL"

    STATUS_CHOICES = [
        (POTENTIAL, "Potential"),
        (ACTUAL, "Actual"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    fix_phone = models.CharField(max_length=12, unique=True)
    mobile_phone = models.CharField(max_length=12, unique=True)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default="POTENTIAL"
    )
    contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def update_date(self):
        self.date_updated = datetime.now()

    def save(self, *args, **kwargs):
        self.update_date()
        return super(Client, self).save()


class Contract(models.Model):
    is_signed = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client} - {self.amount}"

    def update_date(self):
        self.date_updated = datetime.now()

    def save(self, *args, **kwargs):
        self.update_date()
        return super(Contract, self).save()


class Event(models.Model):
    attendees = models.IntegerField(default=0)
    notes = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    contract = models.ForeignKey(
        to=Contract,
        on_delete=models.CASCADE,
    )
    contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.contract} - {self.attendees}"

    def update_date(self):
        self.date_updated = datetime.now()

    def save(self, *args, **kwargs):
        self.update_date()
        return super(Event, self).save()


class Log(models.Model):
    action = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    field = models.CharField(max_length=255, null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
