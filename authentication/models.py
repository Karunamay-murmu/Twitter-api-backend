from django.db import models
from django.utils import timezone

# Create your models here.


class AccessToken(models.Model):

    oauth_token = models.TextField(blank=False, null=True, unique=True)
    oauth_token_secret = models.TextField(blank=False, null=True, unique=True)
    user_id = models.CharField(max_length=255, blank=False, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class meta:
        db_table = "Access Token"
        verbose_name = "Access Token"

    def __str__(self):
        return self.oauth_token

    def get_user_id(self):
        return self.user_id
