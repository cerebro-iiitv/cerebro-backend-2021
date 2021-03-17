from django.contrib import admin
from .models import Faq


class FAQAdmin(admin.ModelAdmin):
    list_display = ("id", "question",)


admin.site.register(Faq)
