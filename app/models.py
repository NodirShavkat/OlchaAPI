from django.db import models
from django.utils import timezone

class Car(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
