# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, Select
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

import fenix

class Profile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=200)

class ExternalTeacher(models.Model):
	PROFESSIONAL_CATEGORIES = (('a', 'Colaborador Não Remunerado Docente'),
				   ('b','Equip.Monitor C/Lic'),
				   ('c','Equip.Prof.Associado Convidado'),
				   ('d','Equip. Assistente Convidado'),
				   ('e','Equiparado Professor Catedrático'),
				   ('f','Equiparado Professor Extraordinário'),
				   ('g','Equiparado Assistente Eventual'),
				   ('h','Segundo Assistente'),
				   ('i','Equiparado Assistente'),
				   ('j','Professor Associado Visitante'),
				   ('k','Professor Catedrático Visitante'),
				   ('l','Assistente Eventual'),
				   ('m','Equiparado Professor Auxiliar'),
				   ('n','Monitor-E.C.D.U. c/Licenciatura'),
				   ('o','Equip.Monitor S/Lic'),
				   ('p','Equip.Assistente Estagiario'),
				   ('q','Equip. Assistente'),
				   ('r','Equip.Prof.Auxiliar Convidado'),
				   ('s','Equip. Prof. Auxiliar'),
				   ('t','Monitor-E.C.D.U.s/Licenciatura'),
				   ('u','Assistente Estagiario'),
				   ('v','Assistente Convidado'),
				   ('w','Assistente'),
				   ('x','Prof Auxiliar Convidado'),
				   ('y','Professor Auxiliar'),
				   ('z','Prof Auxiliar C/Agregação'),
				   ('A','Professor Associado Convidado'),
				   ('B','Professor Associado'),
				   ('C','Professor Associado c/Agregação'),
				   ('D','Professor Catedrático Convidado'),
				   ('E','Professor Catedrático'),)

	ist_id = models.CharField(max_length=20)
	is_closed = models.BooleanField( default=False)
	close_date = models.DateTimeField('close date', null=True)
	professional_category = models.CharField(max_length=1, blank=False, choices=PROFESSIONAL_CATEGORIES)
	hours_per_week = models.DecimalField(decimal_places=2, max_digits=5)
	park = models.BooleanField(default=False)
	card = models.BooleanField(default=False)
	department = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	degree = models.CharField(max_length=200)
	course = models.CharField(max_length=200)
	course_manager = models.CharField(max_length=200)
	notes = models.CharField(max_length=200, blank=True)

	def close(self):
		self.is_closed = True
		self.close_date = datetime.now()

class FenixAPIUserInfo(models.Model):
	user = models.OneToOneField(User)
	code = models.CharField(max_length=200, null=True)
	access_token = models.CharField(max_length=200, blank=True)
	refresh_token = models.CharField(max_length=200, blank=True)
	token_expires = models.IntegerField(default=0)

	def get_fenix_api_user(self):
		user = fenix.User(username=self.user.username, code=self.code, access_token=self.access_token, refresh_token=self.refresh_token, token_expires=self.token_expires)
		return user

