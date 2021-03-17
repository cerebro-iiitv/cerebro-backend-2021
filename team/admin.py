from django.contrib import admin
from team.models import Team


class TeamModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "role",
        "team",
    )
    search_fields = (
        "name",
        "role",
        "team",
    )
    list_filter = ("team",)


admin.site.register(Team, TeamModelAdmin)
