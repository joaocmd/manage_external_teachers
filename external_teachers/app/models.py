from django.db import models

# Create your models here.

class Item(models.Model):
	state = models.BooleanField()
	close_date = models.DateTimeField('close date', null=True)
	##TODO: Add more things...
