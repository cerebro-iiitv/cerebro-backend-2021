from django.contrib import admin

from events.models import Contact, Event


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "short_name",
        "prize",
        "team_size",
    )
    list_display_links = ("title",)
    search_fields = ("title",)


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "name",
        "role",
        "phone_number",
    )
    list_display_links = (
        "role",
        "event",
        "name",
    )
    search_fields = (
        "role",
        "event",
        "name",
    )
    raw_id_fields = ("event",)


admin.site.register(Event, EventAdmin)
admin.site.register(Contact, ContactAdmin)
