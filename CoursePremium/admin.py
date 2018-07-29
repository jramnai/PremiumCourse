# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Premium

class PremiumAdmin(admin.ModelAdmin):
    """
    Admin for the course creator table.
    """

    # Fields to display on the overview page.
    list_display = ['user', 'state']
    # Controls the order on the edit form (without this, read-only fields appear at the end).
    fieldsets = (
        (None, {
            'fields': ['user', 'state']
        }),
    )

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # Store who is making the request.
        obj.admin = request.user
        obj.save()


admin.site.register(Premium, PremiumAdmin) 