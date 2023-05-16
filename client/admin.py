from django.contrib import admin
from client.models import *
# Register your models here.


class Roles_(admin.ModelAdmin):
    list_display =('id','name')

class Profile_(admin.ModelAdmin):
    list_display = ('id','user','username','active_user_role')

admin.site.register(UserRoles, Roles_)
admin.site.register(UserProfile, Profile_)