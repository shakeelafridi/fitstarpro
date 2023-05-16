from django.db import models
from django.urls import reverse

class LandingPageSliderImages(models.Model):
    image = models.ImageField(upload_to='landing_page_slider_image')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class BlogCategories(models.Model):
    name = models.TextField(default='')
    slug = models.TextField(default='')


class Blog(models.Model):
    title = models.TextField(default='')
    featured_image = models.ImageField(upload_to='blog_featured_image')
    second_featured_image = models.ImageField(
        upload_to='blog_featured_image', null=True)
    author = models.TextField(default='')
    video_link = models.TextField(default='')
    author_profile_pic = models.ImageField(upload_to='blog_author_image')
    short_description = models.TextField(default='')
    details = models.TextField(default='')
    category = models.ForeignKey(
        BlogCategories, on_delete=models.CASCADE, null=True)
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class AmbassadorsInfo(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    tagline = models.TextField(default='')
    profile_image = models.ImageField(upload_to='brand_ambassador_image')
    facebook = models.TextField(default='')
    twitter = models.TextField(default='')
    instagram = models.TextField(default='')
    youtube = models.TextField(default='')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class SponsorsInfo(models.Model):
    profile_image = models.ImageField(upload_to='brand_ambassador_image')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CollaboratorsInfo(models.Model):
    profile_image = models.ImageField(upload_to='brand_ambassador_image')
    title = models.TextField(default='')
    sub_title = models.TextField(default='')
    facebook = models.TextField(default='')
    twitter = models.TextField(default='')
    instagram = models.TextField(default='')
    youtube = models.TextField(default='')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class LandingPageDetails(models.Model):
    banner = models.ImageField(upload_to='landing_page')
    banner_text = models.TextField(default='')
    about_us_landing = models.ImageField(upload_to='landing_page')
    about_us_text = models.TextField(default='')
    main_heading = models.TextField(default='')
    sub_heading = models.TextField(default='')
    is_remove = models.BooleanField(default=False)
    footer_about_section = models.TextField(default='')
    footer_phone_no = models.TextField(default='')
    facebook = models.TextField(default='')
    instagram = models.TextField(default='')
    youtube = models.TextField(default='')
    twitter = models.TextField(default='')
    linkedin = models.TextField(default='')
    privacy_policy = models.TextField(default='')
    terms_and_conditionss = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class Specialities(models.Model):
    name = models.TextField(default='')


class Activities(models.Model):
    name = models.TextField(default='')


class Certificationss(models.Model):
    name = models.TextField(default='')


class FitnessCenterTypes(models.Model):
    name = models.TextField(default='')

class SiteSEOLinks(models.Model):
    site_link = models.TextField()
    pub_date = models.DateTimeField(auto_created=True, auto_now_add=True)

    def get_absolute_url(self):
        return self.site_link