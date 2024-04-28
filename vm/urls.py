from django.urls import path
from . import views

urlpatterns = [
    path("vendors/", views.vendor_list, name="vendor-list"),
    path("vendors/<int:pk>/", views.vendor_detail, name="vendor-detail"),
    path("purchase-orders/", views.purchase_order_list, name="purchase-order-list"),
    path(
        "purchase-orders/<int:pk>/",
        views.purchase_order_detail,
        name="purchase-order-detail",
    ),
    path(
        "vendors/<int:vendor_id>/performance/",
        views.vendor_performance,
        name="vendor-performance",
    ),
    path(
        "purchase_orders/<int:po_id>/acknowledge/",
        views.acknowledge_purchase_order,
        name="acknowledge-purchase-order",
    ),
]


"""
URL patterns for the Vendor Management API.

- vendors/ : List all vendors or create a new vendor.
- vendors/<int:pk>/ : Retrieve, update, or delete a specific vendor by its primary key.
- purchase-orders/ : List all purchase orders or create a new purchase order.
- purchase-orders/<int:pk>/ : Retrieve, update, or delete a specific purchase order by its primary key.
- vendors/<int:vendor_id>/performance/ : Retrieve performance metrics for a specific vendor.
- purchase_orders/<int:po_id>/acknowledge/ : Acknowledge a purchase order by its ID.
"""