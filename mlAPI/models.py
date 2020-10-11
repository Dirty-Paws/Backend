from django.db import models

# Create your models here.
class FoodRemainingTimes(models.Model):
    Food_Amount_gr = models.IntegerField()

    Location_Id_1 = models.IntegerField()
    Location_Id_2 = models.IntegerField()
    Location_Id_3 = models.IntegerField()
    Location_Id_4 = models.IntegerField()

    def __int__(self):
        return self.Food_Amount_gr
