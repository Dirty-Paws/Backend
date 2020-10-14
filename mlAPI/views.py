from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import FoodRemainingTimesSerializers
from .models import FoodRemainingTimes
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


@api_view(["POST", "GET"])
def PredictRemainingTime(request):

    # POST METHOD
    if request.method == "POST":
        number_of_locations = 5
        try:

            # Upload the model
            model = pickle.load(open(os.path.join(settings.MODELS, "random_forest.pkl"), 'rb'))

            # Get the data
            data = request.data

            # Create column names
            dictionary = {"Food_Amount_gr": [data["Food_Amount_gr"]]}
            for i in range(1, number_of_locations):
                if i != data["Location_Id"]:
                    dictionary[str(i)] = [0]
                else:
                    dictionary[str(i)] = [1]

            # Create a DataFrame
            df = pd.DataFrame.from_dict(dictionary)

            # Make Prediction
            prediction = model.predict(df.values)

            # Add prediction to the data
            data.update({"Prediction":prediction})

            serializer = FoodRemainingTimesSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(status.HTTP_200_OK)
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

    # GET METHOD
    elif request.method == "GET":

        # Get all remaining times
        data = FoodRemainingTimes.objects.all()

        # Serialize
        serializer = FoodRemainingTimesSerializers(data, many=True)

        return Response(serializer.data)
