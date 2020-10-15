from rest_framework import serializers
from . models import FoodRemainingTimes, Emergency

class FoodRemainingTimesSerializers(serializers.ModelSerializer):
    class Meta:
        model = FoodRemainingTimes
        fields = '__all__'


class EmergencySerializers(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = '__all__'
