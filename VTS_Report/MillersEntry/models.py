from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.

class MillersEntrymodel(models.Model):
    MILLER_TRANSPORTER_ID=models.CharField(max_length=15,primary_key=True)
    MILLER_NAME=models.CharField(max_length=200,blank=True)
    ContactNo=models.CharField(max_length=12,validators=[RegexValidator(r'^\d{10}$', message="Phone number must be 10 digits")],blank=True,)
    district=models.CharField(max_length=200,blank=True)
    class Meta:
        ordering=['MILLER_TRANSPORTER_ID','MILLER_NAME','ContactNo','district',]
    
    def __str__(self):
        return self.MILLER_NAME
    
    
        

    