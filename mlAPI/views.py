from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . serializers import FoodRemainingTimesSerializers
from . models import FoodRemainingTimes
from django.conf import settings

# Create your views here.
import pandas as pd
import numpy as np
import json
import pickle
import os

class FoodRemainingTimesView(viewsets.ModelViewSet):
    queryset = FoodRemainingTimes.objects.all()
    serializer_class = FoodRemainingTimesSerializers

@api_view(["POST"])
def PredictRemainingTime(request):
    try:
        model = pickle.load(open(os.path.join(settings.MODELS, "random_forest.pkl"), 'rb'))
        data = request.data
        values = np.array(list(data.values())).reshape(1, -1)
        prediction = model.predict(values)
        return JsonResponse("Remaining Time is {}".format(prediction), safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
