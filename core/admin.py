from django.contrib import admin
from . import models


@admin.register(models.Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff')
    list_filter = ()


admin.site.register(models.Competitions)
admin.site.register(models.Solutions)
admin.site.register(models.Contests)
admin.site.register(models.Passwords)
admin.site.register(models.Test)
admin.site.register(models.Question)