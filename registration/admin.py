from django.contrib import admin
from registration.models import Dashboard, TeamStatus, TeamMember

admin.site.register(Dashboard)
admin.site.register(TeamMember)
admin.site.register(TeamStatus)