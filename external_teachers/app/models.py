from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=200)


class ExternalTeacher(models.Model):
	is_closed = models.BooleanField()
	close_date = models.DateTimeField('close date', null=True)
	##TODO: Add more things...
