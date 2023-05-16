from django.contrib import admin

# Register your models here.

from .models import SiteSEOLinks

# Register your models here.


class SiteSEOLinksAttributes(admin.ModelAdmin):
    list_display = ('id','site_link')


# Register your models here.
admin.site.register(SiteSEOLinks, SiteSEOLinksAttributes)