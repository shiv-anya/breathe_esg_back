from django.db import models

class Audit(models.Model):
    SOURCE_CHOICES = [
        ('sap', 'SAP'),
        ('utility', 'Utility'),
        ('travel', 'Travel'),
    ]

    name = models.CharField(max_length=255, unique=True)
    source_type = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class RawRow(models.Model):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE)
    raw_data = models.JSONField()

class Activity(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    audit = models.ForeignKey(Audit, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    amount = models.FloatField()
    unit = models.CharField(max_length=50)
    scope = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_flagged = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)