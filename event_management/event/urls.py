from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

router.register('category', CategoryViewSet)
router.register('event', EventsViewsets)


urlpatterns = router.urls + [

    path("bookings/", BookingView.as_view(), name="booking-create"),

    path("my-bookings/<int:booking_id>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),

    path("my-bookings/", MyBookingHistoryView.as_view(), name="my-bookings"),
    path("bookings/<int:booking_id>/status/",BookingView.as_view()),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)