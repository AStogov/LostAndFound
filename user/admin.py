from django.contrib import admin

# Register your models here.
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('openid', 'nick_name', 'avatar', 'gender', 'phone', 'ctime', 'mtime')
    search_fields = ('openid', 'nick_name',  'phone')
