from __future__ import unicode_literals

from uuid import uuid4

from django.contrib.auth.models import get_user_model, AbstractBaseUser
from django.db import models
from django.utils.translation import ugettext as _

User = get_user_model()


class User(AbstractBaseUser):
    name = models.CharField( _("Name of the user"), max_length=70, blank=True )

    class __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

class Question(models.Model):
    title = models.CharField( _("Title of the question") , max_length=130, )
    private = models.BooleanField( _("Is the question private?") )
    user = models.ForeignKey( User, related_name=_("questions") )

    def __unicode__(self):
        return "{} - {}".format(self.title[:50], "Private" if self.private else "Public")

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


class Answer(models.Model):
    body = models.TextField( _("Answer to the question") ) 
    question = models.ForeignKey( Question, related_name=_("answers") )
    user = models.Foreign_key( User, related_name=_("answers") )

    def __unicode__(self):
        return "{} - {}".format(self.body[:50])

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


class TenantManager(models.Manager):
    def create_keys(self, name):
        api_key = uuid4().hex
        tenant = self.model(name=name, api_key=api_key)
        tenant.save()
        return api_key

class Tenant(models.Model):
    name = models.CharField( _("Name of the tenant"), max_length=70, unique=True)
    api_key = models.CharField(max_length=32, unique=True)

    objects = TenantManager()

    class __unicode__(self):
        return "{} - {}".format(self.name, self.api_key)

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")

