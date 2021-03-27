from django.contrib import admin
from registration.models import TeamStatus, TeamMember


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
        "event__title",
        "team__team_code",
        "account__user__email",
    )


class TeamStatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "current_size",
        "is_full",
        "team_code",
    )
    raw_id_fields = ("event",)
    search_fields = (
        "event__title",
        "team_code",
    )
    


admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(TeamStatus, TeamStatusAdmin)