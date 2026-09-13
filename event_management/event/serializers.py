from rest_framework import serializers
from accounts.models import User
from .models import *

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class EventSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    
    category_post = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        source = "category",
        write_only=True
    )
    class Meta:
        model = Events
        fields = [
            'id',
            'title',
            'description',
            'category',
            'category_post',
            'locations',
            'event_date',
            'event_time',
            'total_sets',
            'available_sets',
            'price',
            'Image',
        ]
        
        
class userSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =[
            "id",
            "username",
            "email",
            "phone_number"
        ]
class BookingSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source="user", read_only=True)
    user = userSerializers(read_only=True)
    event = EventSerializers(read_only=True)
    class Meta:
        model = Booking
        fields =[
            "user",
            "event",
            "number_of_tickets",
            "total_price",
            "booking_time",
        ]