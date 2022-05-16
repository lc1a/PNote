from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Estudantes(models.Model):
    Nome= models.CharField(default=None,max_length=255)
    RA= models.CharField(default=None,max_length=255,unique=True)
    Email= models.CharField(default=None,max_length=255)
    CEP= models.CharField(default=None,max_length=255)
    renda=models.FloatField(default=None)
    cod_curso=models.IntegerField(default=None,validators=[MaxValueValidator(9),MinValueValidator(1)])
    escola=models.IntegerField(default=None,validators=[MaxValueValidator(2),MinValueValidator(1)])
    cor=models.IntegerField(default=None,validators=[MaxValueValidator(2),MinValueValidator(1)])
    sexo=models.IntegerField(default=None,validators=[MaxValueValidator(2),MinValueValidator(1)])
    motivacao=models.IntegerField(default=None,validators=[MaxValueValidator(10),MinValueValidator(0)])
    sol_feita=models.BooleanField(default=False,blank=True)

class Solicitacao(models.Model):
    Nome = models.CharField(default=None,max_length=255)
    RA = models.CharField(default=None,max_length=255,unique=True)
    Email = models.CharField(default=None,max_length=255)
    Notebook = models.CharField(default=None,max_length=255,blank=True,null=True)
    Deferida = models.BooleanField(default=None)
    Mensagem = models.CharField(default=None,max_length=255)
    EmailEnviado = models.BooleanField(default=None)
