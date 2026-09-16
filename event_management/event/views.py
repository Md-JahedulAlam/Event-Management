from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.core.files import File
# from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

import qrcode
from io import BytesIO

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminOrReadOnly]

class EventsViewsets(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializers
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields=['price', 'event_date']
    
    def get_queryset(self):
        queryset = Events.objects.all().order_by("-event_date")
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                event_date__gte=timezone.localdate()
            )
        return queryset
    

class BookingView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self, request):
        bookings = Booking.objects.all().order_by("-booking_time")
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        event_id = request.data.get("event")
        number_of_tickets = int(request.data.get("number_of_tickets"))
        
        event = Events.objects.get(id=event_id)
        
        if event.available_sets < number_of_tickets:
            return Response(
                {"error": "Not enough seats available"},
                 status=status.HTTP_400_BAD_REQUEST
            )
        total_price = event.price * number_of_tickets
        
        booking = Booking.objects.create(
            user = request.user,
            event = event,
            number_of_tickets = number_of_tickets,
            total_price=total_price
        )
        
        # QR Code data
        qr_data = f"""
        Booking ID: {booking.id}
        Username: {booking.user.username}
        Email: {booking.user.email}
        
        Event: {booking.event.title}
        Category: {booking.event.category.name}
        Location: {booking.event.locations}
        
        Event Date: {booking.event.event_date}
        Event Time: {booking.event.event_time}
        
        Number of Tickets: {booking.number_of_tickets}
        Price Per Ticket: {booking.event.price}
        Total Price: {booking.total_price}
        
        Booking Date: {booking.booking_time.strftime('%d-%m-%Y')}
        Booking Time: {booking.booking_time.strftime('%I:%M %p')}
        """

        # Generate QR
        qr_image = qrcode.make(qr_data)

        # Save QR in memory
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Save QR to model
        booking.qr_code.save(
            f"booking_{booking.id}.png",
            File(buffer),
            save=True
        )
        
        event.available_sets -= number_of_tickets
        event.save()
        return Response(
             {
                "name" : request.user.username,
                "message": "Ticket booked successfully",
                "tickets": number_of_tickets,
                "price_per_ticket": event.price,
                "total_price": total_price
            },
            status=status.HTTP_201_CREATED
        )

    def patch(self, request, booking_id):
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return Response(
                    {"error": "Booking not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            booking.save()
    
            serializer = BookingSerializer(booking)
    
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
    def get(self, request):
        bookings = Booking.objects.all().order_by("-booking_time")

    
        serializer = BookingSerializer(
            bookings,
            many=True
        )
        return Response(serializer.data)
            
class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, booking_id):

        booking = Booking.objects.get(
            id=booking_id,
            user=request.user
        )

        event = booking.event

        event.available_sets += booking.number_of_tickets
        event.save()

        booking.delete()

        return Response(
            {"message": "Booking cancelled successfully"},
            status=status.HTTP_200_OK
        )
        


class MyBookingHistoryView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["event", "number_of_tickets"]

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).order_by("-booking_time")