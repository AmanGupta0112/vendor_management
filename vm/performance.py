from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Count
from .models import PurchaseOrder


def cal_on_time_del_rate(vendor):

    """
    Calculate the on time delivery rate for the vendor.
    """

    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
    total_completed_pos = completed_pos.count()
    if total_completed_pos == 0:
        return 0
    delivered_on_time = completed_pos.filter(delivery_date__lte=timezone.now()).count()
    return delivered_on_time / total_completed_pos


def cal_qual_rati_avg(vendor):

    """
    Calculate the average quality rating for the vendor.
    """

    completed_pos_with_rating = PurchaseOrder.objects.filter(
        vendor=vendor, status="completed", quality_rating__isnull=False
    )
    rating_count = completed_pos_with_rating.count()
    if rating_count == 0:
        return 0
    return (
        completed_pos_with_rating.aggregate(Avg("quality_rating"))[
            "quality_rating__avg"
        ]
        or 0
    )


def cal_avg_resp_time(vendor):

    """
    Calculate the average response time for the vendor.
    """

    acknowledged_pos = PurchaseOrder.objects.filter(
        vendor=vendor, status="acknowledged"
    )
    response_times = [
        po.acknowledgment_date - po.issue_date
        for po in acknowledged_pos
        if po.acknowledgment_date
    ]
    if not response_times:
        return None
    return sum(response_times, timedelta()) / len(response_times)


def cal_fulfill_rate(vendor):

    """
    Calculate the fulfillment rate for the vendor.
    """

    total_pos_count = PurchaseOrder.objects.filter(vendor=vendor).count()
    if total_pos_count == 0:
        return 0
    successfully_fulfilled_pos_count = PurchaseOrder.objects.filter(
        vendor=vendor, status="completed", issues=None
    ).count()
    return successfully_fulfilled_pos_count / total_pos_count
