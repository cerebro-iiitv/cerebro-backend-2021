from django.contrib import admin
from registration.models import TeamStatus, TeamMember


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "event",
        "team",
    )
    raw_id_fields = (
        "account",
        "event",
        "team",
    )
    search_fields = (
        "event",
        "team",
        "account",
    )


class TeamStatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "current_size",
        "is_full",
        "team_code",
    )
    search_fields = (
        "event",
        "team_code",
    )
    raw_id_fields = ("event",)


admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(TeamStatus, TeamStatusAdmin)