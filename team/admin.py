from django.contrib import admin
from team.models import Team


class TeamModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "role",
    )
    search_fields = (
        "name",
        "role",
    )


admin.site.register(Team, TeamModelAdmin)
