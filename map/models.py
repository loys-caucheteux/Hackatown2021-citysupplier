from django.db import models
from django.contrib.auth.hashers import make_password

class userBase(models.Model):
    name = models.CharField(max_length=100, null=False)
    surname = models.CharField(max_length=100)
    mail = models.EmailField(unique=True, null=False)
    pwd = models.CharField(max_length=200, null=False)
    adress = models.CharField(max_length=200)
    created_on = models.DateField(auto_now_add=True)
    lat = models.DecimalField(null=False, max_digits=25, decimal_places=20, default=0.0)
    lon = models.DecimalField(null=False, max_digits=25, decimal_places=20, default=0.0)
    def __str__(self):
        return '%s %s' % (self.name, self.surname)
    class Meta:
        verbose_name = "utilisateur"

class magBase(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(userBase, unique=False, null=True, on_delete=models.SET_NULL)
    lat = models.DecimalField(null=False, max_digits=25, decimal_places=20, default=0.0)
    lon = models.DecimalField(null=False, max_digits=25, decimal_places=20, default=0.0)
    adress = models.CharField(max_length=200, null=False, default="48 5th Avenue NYC")
    class Meta:
        verbose_name = "magasin"
