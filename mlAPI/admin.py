from django.contrib import admin

# Register your models here.
from .models import FoodRemainingTimes, Emergency, FoodStatus, FoodOrNot

admin.site.register(FoodRemainingTimes)
admin.site.register(Emergency)
admin.site.register(FoodStatus)
admin.site.register(FoodOrNot)