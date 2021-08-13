from users.models import CustomUser
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Hit(models.Model):
    created_by = models.ForeignKey(CustomUser, related_name="CreatedBy", on_delete=models.CASCADE)
    hitman = models.ForeignKey(CustomUser, related_name="AsignedHitman", on_delete=models.CASCADE)
    target_name = models.CharField(max_length=30)
    HIT_STATUS = (
        (0,'Assigned'),
        (1,'Failed'),
        (2,'Completed'),
    )
    status = models.IntegerField(choices=HIT_STATUS, default=0)
    description = models.CharField(max_length=30)