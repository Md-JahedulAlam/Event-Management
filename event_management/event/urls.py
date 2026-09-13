from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()

router.register('category', CategoryViewSet)
router.register('event', EventsViewsets)

# router.register('bookings', BookingView)
# router.register('boookings/<int:id>/cancel/', BookingCancelView)
# router.register('my-booking', MyBookingHistoryView)

urlpatterns = router.urls + [

    path("bookings/", BookingView.as_view(), name="booking-create"),

    path("my-bookings/<int:booking_id>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),

    path("my-bookings/", MyBookingHistoryView.as_view(), name="my-bookings"),
]