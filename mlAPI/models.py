from django.db import models

# Create your models here.
class FoodRemainingTimes(models.Model):

    Food_Amount_gr = models.FloatField(null=True, blank=True)
    Location_Id = models.IntegerField(null=True, blank=True)
    Longitude = models.FloatField(null=True, blank=True)
    Latitude = models.FloatField(null=True, blank=True)
    Prediction = models.FloatField(null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "Food_Amount_gr": self.Food_Amount_gr,
            "Location_Id": self.Location_Id,
            "Longitude": self.Longitude,
            "Latitude": self.Latitude,
            "Prediction": self.Prediction
        }