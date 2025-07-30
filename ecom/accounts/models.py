from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django_countries.fields import CountryField

# Create your models here.
class ShippingAddress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    country = CountryField()
    phone = models.CharField(max_length=100)
    current_address = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100,null=True,blank=True)
    bio = models.TextField(max_length=500, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE,null=True,blank=True, related_name="shipping_address")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

