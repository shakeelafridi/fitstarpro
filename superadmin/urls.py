from django.conf.urls.static import static
from django.urls import path

from FitStarPro.settings import MEDIA_ROOT, MEDIA_URL
from .views import *

app_name = 'superadmin'
urlpatterns = [
    path('login', login, name='login'),

    path('users_listing', users_listing, name='users_listing'),
    path('searchuser', searchuser, name='searchuser'),
    path('change_activeness_user', change_activeness_user,
         name='change_activeness_user'),
    path('delete_user/<int:id>/<str:role>/<int:role_id>', delete_user,
         name='delete_user'),

    path('ambassadors_listing', ambassadors_listing, name='ambassadors_listing'),
    path('delete_ambassador', delete_ambassador, name='delete_ambassador'),
    path('change_activeness_ambassador', change_activeness_ambassador,
         name='change_activeness_ambassador'),

    path('sponsors_listing', sponsors_listing, name='sponsors_listing'),
    path('delete_sponsor', delete_sponsor, name='delete_sponsor'),
    path('change_activeness_sponsor', change_activeness_sponsor,
         name='change_activeness_sponsor'),

    path('collaborators_listing', collaborators_listing,
         name='collaborators_listing'),
    path('delete_collaborator', delete_collaborator, name='delete_collaborator'),
    path('change_activeness_collaborators', change_activeness_collaborators,
         name='change_activeness_collaborators'),

    path('blog_listing', blog_listing, name='blog_listing'),
    path('delete_blog', delete_blog, name='delete_blog'),
    path('change_activeness_blog', change_activeness_blog,
         name='change_activeness_blog'),

    path('landing_page', landing_page, name='landing_page'),
    path('create_user', create_user, name='create_user'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
