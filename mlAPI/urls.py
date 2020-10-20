from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register('mlAPI', views.FoodRemainingTimesView)

urlpatterns = [
                  url(r'^$', views.home, name="home"),
                  path('api/', include(router.urls)),
                  path('remaining/', views.PredictRemainingTime),
                  path('emergency/', views.EmergencyOperations),
                  path('status/', views.FoodStatusOperations),
                  path('isFood/', views.PredictIsFoodOrNot),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
