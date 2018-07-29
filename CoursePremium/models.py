# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# from django.contrib.auth.models import User
from django.db.models.signals import post_init, post_save
from django.utils.translation import ugettext as _
from django.utils import timezone




# # A signal that will be sent when admin should be notified of a pending user request
# send_admin_notification = Signal(providing_args=["user"])

# # A signal that will be sent when user should be notified of change in course creator privileges
# send_user_notification = Signal(providing_args=["user", "state"])

# Create your models here.

class Premium(models.Model):
    """
    Creates the database table model.
    """
    UNREQUESTED = 'unrequested'
    PENDING = 'pending'
    GRANTED = 'granted'
    DENIED = 'denied'

    # Second value is the "human-readable" version.
    STATES = (
        (UNREQUESTED, _(u'unrequested')),
        (PENDING, _(u'pending')),
        (GRANTED, _(u'granted')),
        (DENIED, _(u'denied')),
    )

    # user = models.ForeignKey(User, db_index=True)
    user = models.CharField(max_length=24, blank=False, help_text=_("Username"))
    state = models.CharField(max_length=24, blank=False, choices=STATES, default=UNREQUESTED,
                             help_text=_("Current course creator state"))
    

    def __unicode__(self):
        return u"{0} | {1}".format(self.user, self.state)


