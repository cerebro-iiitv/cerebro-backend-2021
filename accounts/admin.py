from django.contrib import admin
from accounts.models import Account, AuthToken

class AccountAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "user",
        "mobile_number",
        "profile_pic",
    )
    list_display = (
        "id",
        "user",
        "mobile_number",
    )
    list_display_links = (
        "id",
        "user",
        "mobile_number",
    )
    raw_id_fields = ("user",)
    search_fields = ("user", "mobile_number")

admin.site.register(AuthToken)

admin.site.register(Account, AccountAdmin)
