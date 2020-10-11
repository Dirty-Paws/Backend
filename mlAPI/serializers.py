from rest_framework import serializers
from . models import FoodRemainingTimes

class FoodRemainingTimesSerializers(serializers.ModelSerializer):
    class Meta:
        model = FoodRemainingTimes
        fields = '__all__'
