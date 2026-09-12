from rest_framework import serializers
from .models import *

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class EventSerializers(serializers.ModelSerializer):
    # category = CategorySerializers()
    class Meta:
        model = Events
        fields = '__all__'