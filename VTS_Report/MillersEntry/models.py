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
    
    def save(self, *args, **kwargs):
        from logmodels.models import MillersEntryLogModel
        
        # Check if this is a creation or update
        if self._state.adding:  # True if this is a new instance (creation)
            action = "Created"
        else:
            action = "Updated"
        
        # Save the MillersEntrymodel instance
        super(MillersEntrymodel, self).save(*args, **kwargs)
        
        # Log the action
        MillersEntryLogModel.objects.create(
            miller_entry=self,
            action=action,
            timestamp=timezone.now(),
            description=f"Miller Entry {action}: {self.MILLER_TRANSPORTER_ID} - {self.MILLER_NAME}"
        )

    