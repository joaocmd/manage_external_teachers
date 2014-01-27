from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea

class Profile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=200)


class ExternalTeacher(models.Model):
	user = models.ForeignKey(User)
	is_closed = models.BooleanField()
	close_date = models.DateTimeField('close date', null=True)
	professional_category = models.CharField(max_length=200, blank=False)
	hours_per_week = models.DecimalField(decimal_places=2, max_digits=5)
	park = models.BooleanField()
	card = models.BooleanField()
	department = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	degree = models.CharField(max_length=200)
	course = models.CharField(max_length=200)
	course_manager = models.CharField(max_length=200)
	notes = models.CharField(max_length=200, blank=True)

class ExternalTeacherForm(ModelForm):
	class Meta:
		model = ExternalTeacher
		fields = '__all__'
		exclude = ('close_date', )
		widgets = {'notes' : Textarea(), }
