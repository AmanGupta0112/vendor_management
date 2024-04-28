from django.db import models
from django.utils import timezone


class Vendor(models.Model):
    """
    Model representing a vendor.
    """

    name = models.CharField(max_length=100, help_text="Name of the vendor")
    contact_details = models.TextField(help_text="Contact details of the vendor")
    address = models.TextField(help_text="Address of the vendor")
    vendor_code = models.CharField(
        max_length=50, unique=True, help_text="Unique code for the vendor"
    )

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    """
    Model representing a purchase order.
    """

    class StatusChoices(models.TextChoices):
        DRAFT = "draft", "Draft"
        COMPLETED = "completed", "Completed"
        ACKNOWLEDGED = "acknowledged", "Acknowledged"
        # Add more status choices as needed

    po_number = models.CharField(
        max_length=100, unique=True, help_text="Unique identifier for the PO"
    )
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, help_text="Vendor associated with the PO"
    )
    order_date = models.DateTimeField(
        db_index=True, help_text="Date when the PO was ordered"
    )
    delivery_date = models.DateTimeField(
        db_index=True, help_text="Expected delivery date of the PO"
    )
    items = models.JSONField(help_text="Items included in the PO")
    quantity = models.IntegerField(help_text="Quantity of items in the PO")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
        db_index=True,
        help_text="Status of the PO",
    )
    quality_rating = models.FloatField(
        null=True,
        blank=True,
        help_text="Quality rating of the PO (if available)",
    )
    issue_date = models.DateTimeField(
        default=timezone.now, db_index=True, help_text="Date when the PO was issued"
    )
    acknowledgment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date when the PO was acknowledged by the vendor",
    )

    def __str__(self):
        return self.po_number


class HistoricalPerformance(models.Model):
    """
    Model representing historical performance data of vendors.
    """

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        help_text="Vendor associated with the performance data",
    )
    date = models.DateTimeField(
        default=timezone.now, help_text="Date when the performance data was recorded"
    )
    on_time_delivery_rate = models.FloatField(
        default=0, help_text="Historical on-time delivery rate of the vendor"
    )
    quality_rating_avg = models.FloatField(
        default=0, help_text="Historical average quality rating of the vendor"
    )
    average_response_time = models.FloatField(
        default=0,
        help_text="Historical average response time of the vendor for POs",
    )
    fulfillment_rate = models.FloatField(
        default=0, help_text="Historical fulfillment rate of the vendor"
    )

    def __str__(self):
        return f"{self.vendor} - {self.date}"
