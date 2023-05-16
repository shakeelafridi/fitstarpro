from os import name
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import settings
#SEO
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from superadmin.models import SiteSEOLinks

info_dict = {
    'queryset': SiteSEOLinks.objects.all(),
    'date_field': 'pub_date',
    'site_link' : 'site_link',
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('client.urls')),
    # path('', include('django.contrib.auth.urls')),
    path('accounts/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='client/accounts/forgot_password_confirm.html'), name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetView.as_view(
        template_name='client/accounts/forgot_password_done.html'), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='client/accounts/forgot_password_complete.html'), name='password_reset_complete'),
    path('superadmin/', include('superadmin.urls')),
    #SEO link confiugrations

    # path('sitemap/', site_links, name='sitemap'),

    path('sitemap.xml', sitemap,
         {'sitemaps': {'site_links': GenericSitemap(info_dict, priority=0.9)}},
         name='django.contrib.sitemaps.views.sitemap'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
