from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser, Subscribe


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subscriptions',
    )
    list_per_page = 15
    list_display_links = ('user',)


UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('avatar',)}),
)
admin.site.register(MyUser, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
