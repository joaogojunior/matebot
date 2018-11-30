from django.db import models
from django.contrib.auth.models import User

from django.utils.timezone import now
# Create your models here.
#from django.utils.translation import ugettext_lazy as _

class Dado(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    idade = models.IntegerField(default=0)
    sexo = models.TextField(default="")
    filename = models.TextField(default="")
    tamanho = models.FloatField(default=0.0)
    texto = models.TextField(default="")
    polarity = models.FloatField(default=0.0)
    numsil = models.IntegerField(default=0)
    silabas = models.TextField(default="")
    vel = models.FloatField(default=0.0)
    data = models.DateTimeField(default=now, blank=True)
    ipaddr = models.GenericIPAddressField(default='0.0.0.0')
    geo=models.TextField(default="")
    latitude=models.FloatField(default=0.0)
    longitude=models.FloatField(default=0.0)
    rotulo=models.TextField(default="")