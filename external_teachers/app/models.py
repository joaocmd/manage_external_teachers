from django.db import models

# Create your models here.

class ExternalTeacher(models.Model):
	is_closed = models.BooleanField()
	close_date = models.DateTimeField('close date', null=True)
	##TODO: Add more things...
