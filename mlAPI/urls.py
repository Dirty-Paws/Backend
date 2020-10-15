from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('mlAPI', views.FoodRemainingTimesView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('remaining/', views.PredictRemainingTime),
    path('emergency/', views.EmergencyOperations),
]
