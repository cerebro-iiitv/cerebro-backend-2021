from django.contrib import admin
from accounts.models import Account, AuthToken


class AccountAdmin(admin.ModelAdmin):
    # readonly_fields = (
    #     "id",
    #     "user",
    #     "mobile_number",
    #     "profile_pic",
    # )
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


class AuthTokenAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "user",
        "key",
    )
    list_display = (
        "id",
        "user",
        "key",
    )
    list_display_links = (
        "id",
        "user",
        "key",
    )
    raw_id_fields = ("user",)
    search_fields = ("user",)


admin.site.register(AuthToken, AuthTokenAdmin)
admin.site.register(Account, AccountAdmin)
