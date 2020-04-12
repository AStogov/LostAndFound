from django.contrib import admin

# Register your models here.
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('openid', 'name', 'card', 'phone', 'contact', 'ctime', 'mtime')
    search_fields = ('openid', 'name',  'phone', 'card')
