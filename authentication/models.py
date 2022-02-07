from tabnanny import verbose
from django.db import models

# Create your models here.

class Token(models.Model):

    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    class meta:
        db_table = "token"
        verbose_name = "Token"

    def __str__(self):
        return self.access_token

    def access_token(self):
        return self.access_token

    def refresh_token(self):
        return self.refresh_token