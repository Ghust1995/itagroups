from django.db import models

# Create your models here.
class Group(models.Model):
	name = models.TextField(default = '')
	alias = models.TextField(default = '')
	tags = models.TextField(default = '')
	description = models.TextField(default = '')

class User(models.Model):
	access_token = models.TextField(default = '')
	apelido = models.TextField(default = '')
	turma = models.TextField(default = '')
	groups = models.ManyToManyField(Group)