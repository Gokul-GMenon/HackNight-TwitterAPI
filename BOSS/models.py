from django.db import models

# Create your models here.
class DataField(models.Model):

    name = models.TextField()
    user_id = models.PositiveBigIntegerField()
    
    def __str__(self):
        return self.name