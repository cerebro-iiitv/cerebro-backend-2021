from django.contrib import admin
from accounts.models import Account


class AccountAdmin(admin.ModelAdmin):
    readonly_fields = (
        "first_name",
        "last_name",
        "email",
        "mobile_number",
        "profile_pic",
    )
    list_display = (
        "first_name",
        "last_name",
        "email",
        "mobile_number",
    )
    list_display_links = (
        "first_name",
        "email",
        "last_name",
    )
    search_fields = ("first_name", "last_name", "email", "mobile_number")


admin.site.register(Account, AccountAdmin)
