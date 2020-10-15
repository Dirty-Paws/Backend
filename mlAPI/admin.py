from django.contrib import admin

# Register your models here.
from . models import FoodRemainingTimes, Emergency

admin.site.register(FoodRemainingTimes)
admin.site.register(Emergency)