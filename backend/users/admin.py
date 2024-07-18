from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .constants import LIST_PER_PAGE
from .models import MyUser, Subscribe


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subscriptions',
    )
    list_per_page = LIST_PER_PAGE
    list_display_links = ('user',)


UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('avatar',)}),
)
admin.site.register(MyUser, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
