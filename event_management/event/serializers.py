from rest_framework import serializers
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