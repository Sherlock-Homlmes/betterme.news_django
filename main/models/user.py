from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
#import datetime, pytz
from django.utils.timezone import now


class Employee(models.Model):
    CITY = [
        (0,"Choose"),
        (29,"Ha Noi"),
        (90, "Ha Nam")
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    birthday = models.DateField(default = now)
    email = models.EmailField(max_length=254)
    phone = models.BigIntegerField(
        blank=True
    )
    city = models.IntegerField(
        choices= CITY,
        default= 0,
    )
    password = models.CharField(max_length=100)

class DiscordUser(models.Model):
    pass
class GoogleUser(models.Model):
    pass
class FacebookUser(models.Model):
    pass