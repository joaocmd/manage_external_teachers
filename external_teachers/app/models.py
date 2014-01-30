from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from django.forms import ModelForm, Textarea, Select

import fenix

class Profile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=200)


class ExternalTeacher(models.Model):
	user = models.ForeignKey(User)
	is_closed = models.BooleanField(default=False)
	close_date = models.DateTimeField('close date', null=True)
	professional_category = models.CharField(max_length=200, blank=False)
	hours_per_week = models.DecimalField(decimal_places=2, max_digits=5)
	park = models.BooleanField(default=False)
	card = models.BooleanField(default=False)
	department = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	degree = models.CharField(max_length=200)
	course = models.CharField(max_length=200)
	course_manager = models.CharField(max_length=200)
	notes = models.CharField(max_length=200, blank=True)

class FenixAPIUserInfo(models.Model):
	user = models.OneToOneField(User)
	code = models.CharField(max_length=200, null=True)
	access_token = models.CharField(max_length=200, blank=True)
	refresh_token = models.CharField(max_length=200, blank=True)
	token_expires = models.IntegerField(default=0)

	def get_fenix_api_user(self):
		user = fenix.User(username=self.user.username, code=self.code, access_token=self.access_token, refresh_token=self.refresh_token, token_expires=self.token_expires)
		return user

