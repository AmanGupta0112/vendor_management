from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.utils import timezone
from .serializers import VendorPerformanceSerializer
from .serializers import VendorSerializer, PurchaseOrderSerializer
from .performance import (
    cal_on_time_del_rate,
    cal_qual_rati_avg,
    cal_avg_resp_time,
    cal_fulfill_rate,
)


@api_view(["GET", "POST"])
def vendor_list(request):

    """
    API endpoint to list all vendors or create a new vendor.

    GET:
    Returns a JSON response with a list of all vendors.

    POST:
    Creates a new vendor based on the provided data.
    """

    if request.method == "GET":
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == "POST":
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def vendor_detail(request, pk):
    
    """
    API endpoint to retrieve, update, or delete a specific vendor.

    GET:
    Retrieves the details of the specified vendor.

    PUT:
    Updates the details of the specified vendor.

    DELETE:
    Deletes the specified vendor.
    """

    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return JsonResponse({"error": "Vendor not found"}, status=404)

    if request.method == "GET":
        serializer = VendorSerializer(vendor)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        vendor.delete()
        return JsonResponse({"message": "Vendor deleted successfully"}, status=204)


@api_view(["GET", "POST"])
def purchase_order_list(request):

    """
    API endpoint to list all purchase orders or create a new purchase order.

    GET:
    Returns a JSON response with a list of all purchase orders.

    POST:
    Creates a new purchase order based on the provided data.
    """

    if request.method == "GET":
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def purchase_order_detail(request, pk):

    """
    API endpoint to retrieve, update, or delete a specific purchase order.

    GET:
    Retrieves the details of the specified purchase order.

    PUT:
    Updates the details of the specified purchase order.

    DELETE:
    Deletes the specified purchase order.
    """

    try:
        purchase_order = PurchaseOrder.objects.get(pk=pk)
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({"error": "Purchase order not found"}, status=404)

    if request.method == "GET":
        serializer = PurchaseOrderSerializer(purchase_order)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        purchase_order.delete()
        return JsonResponse(
            {"message": "Purchase order deleted successfully"}, status=204
        )


@api_view(["GET"])
def vendor_performance(request, vendor_id):

    """
    API endpoint to retrieve the historical performance data for a specific vendor.

    GET:
    Retrieves the historical performance data for the specified vendor.
    """

    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return JsonResponse({"error": "Vendor not found"}, status=404)

    # Retrieve historical performance data
    try:
        historical_performance = HistoricalPerformance.objects.get(vendor=vendor)
    except HistoricalPerformance.DoesNotExist:
        return JsonResponse(
            {"error": "Historical performance data not found"}, status=404
        )

    serializer = VendorPerformanceSerializer(historical_performance)
    return JsonResponse(serializer.data)


# Endpoint for vendors to acknowledge POs
@api_view(["POST"])
def acknowledge_purchase_order(request, po_id):

    """
    API endpoint for vendors to acknowledge purchase orders.

    POST:
    Acknowledges the specified purchase order and recalculates average response time for the vendor.
    """

    try:
        po = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({"error": "Purchase order not found"}, status=404)

    po.acknowledgment_date = timezone.now()
    po.save()

    # Recalculate average response time
    vendor = po.vendor
    vendor.average_response_time = cal_avg_resp_time(vendor)
    vendor.save()

    return JsonResponse({"message": "Purchase order acknowledged successfully"})
