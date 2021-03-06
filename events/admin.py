from django.contrib import admin

from events.models import Contact, Event

admin.site.register(Event)
admin.site.register(Contact)
