from django.db import models

# Create your models here.
class Captura(models.Model):
	code = models.CharField(max_length=15)
	code_user = models.CharField(max_length=15)
	active = models.IntegerField()
	name = models.CharField(max_length=100) 
	age = models.IntegerField()
	sex = models.CharField(max_length=10)
	curso = models.CharField(max_length=100)
	periodo = models.CharField(max_length=15)
	matricula = models.CharField(max_length=20)	

	def __str__(self):
		return self.code
