from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views

from FitStarPro.settings import MEDIA_ROOT, MEDIA_URL
from .views import *

app_name = 'client'
urlpatterns = [
    path('accounts/login', login, name='login'),
    # path('accounts/forgot_password', auth_views.PasswordResetView.as_view(
    #     template_name='client/accounts/forgot_password.html'), name='forgot_password'),

    path('accounts/forgot_password', password_reset_request, name='forgot_password'),
    path('confirm_email', password_reset_request, name='confirm_email'),
    path('accounts/forgot_password/done', auth_views.PasswordResetDoneView.as_view(
        template_name='client/accounts/forgot_password_done.html'), name='forgot_password_done'),
    path('accounts/forgot_password_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='client/accounts/forgot_password_confirm.html'), name='forgot_password_confirm'),
    path('accounts/forgot_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='client/accounts/forgot_password_complete.html'), name='forgot_password_complete'),
    path('accounts/logout', logout, name='logout'),
    path('accounts/register', register, name='register'),





    path('', home, name='home'),
    path('about-us', about_us, name='about_us'),
    path('blog', blog, name='blog'),
    path('fitness-pros', fitness_pros, name='fitness_pros'),
    path('fitness-center', fitness_center, name='fitness_center'),
    path('fitness-models', fitness_models, name='fitness_models'),
    path('blog-details', blog_details, name='blog_details'),
    path('contact-us', contact_us, name='contact_us'),
    path('user-contact_us', user_contact_us, name='user_contact_us'),
    path('privacy-policy', privacy_policy, name='privacy_policy'),
    path('terms-and-conditions', terms_and_conditions,
         name='terms_and_conditions'),

    path('accounts/details', profile, name='profile'),
    path('profile-page', profile_page, name='profile_page'),
    path('center/<str:unique>', center_profile, name='center_profile'),
    path('pro/<str:unique>', pro_profile, name='profile_page'),
    path('Professional-Sponsers-Update', Professional_Sponsers_Update,
         name='Professional_Sponsers_Update'),
    path('Delete-professional-Sponser', Delete_professional_Sponser,
         name='Delete_professional_Sponser'),
    path('model/<str:unique>', modal_profile, name='modal_profile'),

    # path('professional/<str:prof>/', professional, name='professional'),
    # path('modal/<str:modal>/', modal, name='modal'),
    # path('center/<str:center>/', center, name='center'),

    path('top-bar-info-update', top_bar_info_update, name='top_bar_info_update'),
    path('about-info-update', about_info_update, name='about_info_update'),
    path('update-profile-image', update_profile_image,
         name='update_profile_image'),
    path('update_user_role', update_user_role, name='update_user_role'),

    path('update-location-info', update_location_info,
         name='update_location_info'),

    path('update-info-tab', update_info_tab, name='update_info_tab'),
    path('portfolio-update', portfolio_update, name='portfolio_update'),
    path('portfolio-update-gallery', portfolio_update_gallery,
         name='portfolio_update_gallery'),
    path('delete-portfolio-gallery-image', delete_portfolio_gallery_image,
         name='delete_portfolio_gallery_image'),
    path('delete-success-story', delete_success_story,
         name='delete_success_story'),
     path('delete_video_link_pro/', delete_video_link_pro,
         name='delete_video_link_pro'),
    path('delete-ad-information', delete_ad_information,
         name='delete_ad_information'),
    path('update-contact-info-tab', update_contact_info_tab,
         name='update_contact_info_tab'),
    path('ads-info-tab-update', ads_info_tab_update, name='ads_info_tab_update'),
    path('edit-ads-info-tab-update', edit_ads_info_tab_update,
         name='edit_ads_info_tab_update'),
    path('about-rating-submit', about_rating_submit,
         name='about_rating_submit'),

    path('data-dump', data_dump, name='data_dump'),
    path('heart_counter/', heart_counter, name='heart_counter'),
    path('blog_heart_counter/', blog_heart_counter, name='blog_heart_counter'),
    
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
