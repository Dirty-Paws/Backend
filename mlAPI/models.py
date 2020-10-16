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
            "Food_Amount_gr": self.Food_Amount_gr,
            "Location_Id": self.Location_Id,
            "Longitude": self.Longitude,
            "Latitude": self.Latitude,
            "Prediction": self.Prediction
        }


class Emergency(models.Model):
    message = models.CharField(max_length=200, null=True, blank=True)
    owner_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    Location_Id = models.IntegerField(null=True, blank=True)
    Longitude = models.FloatField(null=True, blank=True)
    Latitude = models.FloatField(null=True, blank=True)

    def serialize(self):
        return {
            "message": self.message,
            "owner_id": self.owner_id,
            "user_id": self.owner_id,
            "status": self.status,
            "image": self.image,
            "Location_Id": self.Location_Id,
            "Longitude": self.Longitude,
            "Latitude": self.Latitude,
        }
