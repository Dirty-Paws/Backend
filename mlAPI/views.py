from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import FoodRemainingTimesSerializers, EmergencySerializers, FoodStatusSerializers, FoodOrNotSerializers
from .models import FoodRemainingTimes, Emergency, FoodStatus, FoodOrNot
from django.conf import settings

import pandas as pd
import numpy as np
import pickle
import os

from io import BytesIO

from PIL import Image
from keras.models import model_from_json
from keras.preprocessing import image
import urllib
import requests

# HomePage
def home(request):
    template = "home.html"
    context = {}
    return render(request, template, context)


# Food Remaining Times
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
            dictionary = {"Food_Amount_gr": [float(data["Food_Amount_gr"])]}
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
            data.update({"Prediction": float(prediction)})

            # Save the data
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


# Emergency Handling
class EmergencyView(viewsets.ModelViewSet):
    queryset = Emergency.objects.all()
    serializer_class = EmergencySerializers


@api_view(["POST", "GET"])
def EmergencyOperations(request):
    # GET METHOD
    if request.method == 'GET':
        emergencies = Emergency.objects.all()
        serializer = EmergencySerializers(emergencies, many=True)
        return Response(serializer.data)

    # POST METHOD
    elif request.method == 'POST':
        serializer = EmergencySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Food Status
class FoodStatusView(viewsets.ModelViewSet):
    queryset = FoodStatus.objects.all()
    serializer_class = FoodStatusSerializers


@api_view(["POST", "GET"])
def FoodStatusOperations(request):
    try:

        # GET METHOD
        if request.method == 'GET':
            food_status = FoodStatus.objects.all()
            serializer = FoodStatusSerializers(food_status, many=True)
            return Response(serializer.data)

        # POST METHOD
        elif request.method == 'POST':

            data = request.data
            try:
                location = FoodStatus.objects.get(Location_Id=data["Location_Id"])
                for key, value in data.items():
                    setattr(location, key, value)
                location.save()
            except FoodStatus.DoesNotExist:
                data.update({'IsFoodFinished': data["IsFoodFinished"]})
                location = FoodStatus(**data)
                location.save()

            return Response(status.HTTP_200_OK)
    except Exception as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


# Food Or Not
class FoodOrNotView(viewsets.ModelViewSet):
    queryset = FoodOrNot.objects.all()
    serializer_class = FoodOrNotSerializers

# Load and Preprocess
def load_process(img_url):

    # IF 0 IS FOOD
    # IF 1 IS NOT FOOD

    img_url = img_url.strip('\'"')
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((224,224))
    img = image.img_to_array(img)
    img = img / 255
    dictionary = {"Image":img}
    value = np.array(dictionary["Image"])
    value = value.reshape(1, 224, 224, 3)
    return value

@api_view(["POST", "GET"])
def PredictIsFoodOrNot(request):

    # POST METHOD
    if request.method == "POST":
        try:

            # Upload the model
            json_file = open(os.path.join(settings.MODELS, "isfood_model.json"), 'rb')
            loaded_model_json = json_file.read()
            json_file.close()
            model = model_from_json(loaded_model_json)

            # Load weights into the model
            model.load_weights(os.path.join(settings.MODELS, "is_foodweights.h5"))

            # Compile the model
            model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])

            # Get the data
            data = request.data

            # Get the image from data
            bowl_image_url = data["ImageBowl"]

            # Get the image and make preprocessing
            final_img = load_process(bowl_image_url)

            # Make Prediction
            prediction = model.predict(final_img)

            # Add prediction to the data
            data.update({"IsFood": int(not int(prediction))})

            # Save the data
            serializer = FoodOrNotSerializers(data=data)

            if serializer.is_valid():
                serializer.save()

            return Response(status.HTTP_200_OK)
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

    # GET METHOD
    elif request.method == "GET":

        # Get all remaining times
        data = FoodOrNot.objects.all()

        # Serialize
        serializer = FoodOrNotSerializers(data, many=True)

        return Response(serializer.data)
