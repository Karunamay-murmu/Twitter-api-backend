from email.policy import default
from os import access
from django.db import models
from django.utils.translation import gettext_lazy as _


class Account(models.Model):

    screen_name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(_("User's full name"), max_length=255, blank=False, null=False)
    picture = models.URLField(_("User's profile picture"), max_length=200)
    twitter_user_id = models.CharField(max_length=255, unique=True, blank=False, null=False)
    access_token = models.TextField(blank=False, null=False)
    access_token_secret = models.TextField(blank=False, null=False)
    last_ip = models.GenericIPAddressField(blank=True, null=True)
    # data = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_access_token(self):
        return self.access_token

    def to_dict(self):
        return {
            "username": self.screen_name,
            "nickname": self.nickname,
            "name": self.name,
            "profile_image_url": self.picture,
            "twitter_id": self.twitter_user_id,
        }

    class Meta:
        verbose_name = _("Twitter User")
        verbose_name_plural = _("Twitter Users")
        ordering = ["-twitter_user_id"]

