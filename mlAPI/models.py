from django.db import models


# Create your models here.
class FoodRemainingTimes(models.Model):
    Food_Amount_gr = models.FloatField(null=True, blank=True)
    Location_Id = models.IntegerField(null=True, blank=True)
    Longitude = models.FloatField(null=True, blank=True)
    Latitude = models.FloatField(null=True, blank=True)
    Prediction = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.Food_Amount_gr} {self.Location_Id} {self.Longitude} {self.Latitude} {self.Location_Id} {self.Prediction}"

class Emergency(models.Model):
    message = models.CharField(max_length=200, null=True, blank=True)
    owner_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    Location_Id = models.IntegerField(null=True, blank=True)
    Longitude = models.FloatField(null=True, blank=True)
    Latitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.message} {self.owner_id} {self.user_id} {self.status} {self.image} {self.Location_Id} {self.Longitude} {self.Latitude}"

class FoodStatus(models.Model):

    IsFoodFinished = models.IntegerField(null=True, blank=True)
    Location_Id = models.IntegerField(null=True, blank=True)
    Longitude = models.FloatField(null=True, blank=True)
    Latitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.IsFoodFinished} {self.Location_Id} {self.Longitude} {self.Latitude}"
