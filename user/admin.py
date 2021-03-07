from django.contrib import admin

# Register your models here.
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'openid', 'qq', 'cardno', 'phone', 'wxid', 'created_at', 'modified_at', 'history', 'favored')
    search_fields = ('id', 'openid', 'qq',  'phone', 'cardno', 'wxid')
