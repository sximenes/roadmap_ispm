from django.db import models


class Test(models.Model):
    teste = models.CharField(max_length=200)
