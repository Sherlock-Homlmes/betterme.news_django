from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
class Comment(models.Model):

    positon = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(primary_key=True)
    rate = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
        )
    comment = models.CharField(max_length=1000)
    date = models.DateField(default=datetime.datetime.now)

    def __str__(self):
        return self.comment

    def get_comment(self,position):
        pass