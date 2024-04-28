from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor, HistoricalPerformance
from .performance import (
    cal_on_time_del_rate,
    cal_qual_rati_avg,
    cal_avg_resp_time,
    cal_fulfill_rate,
)

@receiver([post_save, post_delete], sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    """
    Signal receiver function to update vendor performance metrics upon changes in purchase orders.

    Parameters:
        sender: The sender of the signal.
        instance: The instance of the PurchaseOrder model that triggered the signal.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """

    vendor = instance.vendor

    # Calculate performance metrics
    on_time_delivery_rate = cal_on_time_del_rate(vendor)
    quality_rating_avg = cal_qual_rati_avg(vendor)
    average_response_time = cal_avg_resp_time(vendor)
    fulfillment_rate = cal_fulfill_rate(vendor)

    # Create or update HistoricalPerformance
    HistoricalPerformance.objects.update_or_create(
        vendor=vendor,
        defaults={
            "on_time_delivery_rate": on_time_delivery_rate,
            "quality_rating_avg": quality_rating_avg,
            "average_response_time": average_response_time,
            "fulfillment_rate": fulfillment_rate,
        },
    )
