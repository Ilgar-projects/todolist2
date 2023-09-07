from django.contrib import admin
from django.utils.html import format_html
from bot.models import TgUser
from django.urls import reverse


# admin.site.register(TgUser)


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'tg_user')
    readonly_fields = ['verification_code']
    search_fields = ['chat_id', 'username']

    def tg_user(self, obj: TgUser) -> str | None:
        if user := obj.user:
            return format_html(
                '<a href="{url}">{username}</a>',
                url=reverse('admin:core_user_change', kwargs={'object_id': user.id}),
                username=user.username
            )
