from django.db import models
from django.contrib.auth.models import User
from numpy import mod


class UserRoles(models.Model):
    name = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(UserRoles)
    time_zone_info = models.TextField(default='')
    city = models.TextField(default='')
    country = models.TextField(default='')
    referred = models.TextField(default='')
    state = models.TextField(default='')
    location = models.TextField(default='')
    gender = models.TextField(default='')
    username = models.TextField(default='')
    sign_up_role = models.ForeignKey(
        UserRoles, on_delete=models.CASCADE, related_name='sign_up_role', null=True)
    active_user_role = models.ForeignKey(UserRoles, on_delete=models.CASCADE, related_name='active_user_role',
                                         null=True)
    date_of_birth = models.DateField(null=True)
    profile_image = models.ImageField(upload_to='profile_image', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FitnessCenterMemberShipType(models.Model):
    name = models.TextField(default='')


class FitnessCenterType(models.Model):
    name = models.TextField(default='')


class TimeZone(models.Model):
    name = models.TextField(default='')


class EthnicityTypes(models.Model):
    name = models.TextField(default='')


class SkinTone(models.Model):
    name = models.TextField(default='')


class EyeColor(models.Model):
    name = models.TextField(default='')


class Countries(models.Model):
    name = models.TextField(default='')


class HairColor(models.Model):
    name = models.TextField(default='')


class Tattoos(models.Model):
    name = models.TextField(default='')


class BodyTypes(models.Model):
    name = models.TextField(default='')


class DietTypes(models.Model):
    name = models.TextField(default='')


class ClientPreferences(models.Model):
    name = models.TextField(default='')


class ModellingInterests(models.Model):
    name = models.TextField(default='')


class Compensation(models.Model):
    name = models.TextField(default='')


class SuccessStories(models.Model):
    before = models.ImageField(upload_to='success_stories')
    after = models.ImageField(upload_to='success_stories', null=True)
    description = models.TextField(default='')
    instagram_link = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class AdsInformation(models.Model):
    image = models.ImageField(upload_to='success_stories')
    session_name = models.TextField(default='')
    activity = models.TextField(default='')
    intensity_level = models.IntegerField(default=0)
    days = models.TextField(default='')
    time = models.TextField(default='')
    location = models.TextField(default='')
    description = models.TextField(default='')
    price = models.TextField(default='')
    spots_available = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    comment = models.TextField(max_length=150)


class FitnessProfessionalProfile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_image', null=True)
    name = models.TextField(default='')
    sponser_text = models.TextField(default='')
    sponsor_names = models.TextField(default='')
    profile_url = models.TextField(default='')
    about_us = models.TextField(default='')
    brands = models.TextField(default='')
    video_code = models.TextField(default='')
    video_code2 = models.TextField(default='')
    video_code3 = models.TextField(default='')
    video_code4 = models.TextField(default='')
    height = models.TextField(default='')
    weight = models.TextField(default='')
    height_unit = models.TextField(default='')
    weight_unit = models.TextField(default='')
    age = models.TextField(default='')
    training_rates = models.TextField(default='')
    experience = models.TextField(default='')
    languages = models.TextField(default='')
    body_type = models.TextField(default='')
    business_name = models.TextField(default='')
    client_preferences = models.TextField(default='')
    # 0 for not selected
    # 1 for yes
    # 2 for no
    availability_for_on_line_training = models.IntegerField(default=0)
    availability_for_in_home_training = models.IntegerField(default=0)
    note_about_training_rates = models.CharField(default='', max_length=999)
    training_methods_and_styles = models.CharField(default='', max_length=999)
    fitness_awards = models.TextField(default='')
    sponsor_brands = models.TextField(default='')
    degree = models.TextField(default='')
    profession = models.TextField(default='')
    certifications = models.TextField(default='')
    specialities = models.TextField(default='')
    activities = models.TextField(default='')
    diet_type = models.TextField(default='')
    facebook = models.TextField(default='')
    instagram = models.TextField(default='')
    youtube = models.TextField(default='')
    twitter = models.TextField(default='')
    blog_link = models.TextField(default='')
    booking_link = models.TextField(default='')
    portal_link = models.TextField(default='')
    vimeo_link = models.TextField(default='')
    other_link = models.TextField(default='')
    website = models.TextField(default='')
    phone_number = models.TextField(default='')
    address = models.TextField(default='')
    address2 = models.TextField(default='')
    address3 = models.TextField(default='')
    gym_used = models.TextField(default='')
    gym_used2 = models.TextField(default='')
    gym_used3 = models.TextField(default='')
    reviews = models.IntegerField(default=0)
    number_of_reviews = models.IntegerField(default=0)
    product_reviews = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ManyToManyField(Comments)


class FitnessCenterProfile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    open_since = models.IntegerField(default=0)
    name = models.TextField(default='')
    about_us = models.TextField(default='')
    brands = models.TextField(default='')
    video_code = models.TextField(default='')
    video_code2 = models.TextField(default='')
    video_code3 = models.TextField(default='')
    video_code4 = models.TextField(default='')
    specialities = models.TextField(default='')
    languages = models.TextField(default='')
    profile_url = models.TextField(default='')
    hours_of_operation = models.TextField(default='')
    awards = models.TextField(default='')
    profile_image = models.ImageField(upload_to='profile_image', null=True)
    member_ship_plans = models.TextField(default='')
    fitness_center_type = models.ForeignKey(
        FitnessCenterType, on_delete=models.CASCADE, null=True)
    fitness_pros = models.ManyToManyField(FitnessProfessionalProfile)
    facebook = models.TextField(default='')
    instagram = models.TextField(default='')
    youtube = models.TextField(default='')
    twitter = models.TextField(default='')
    blog_link = models.TextField(default='')
    booking_link = models.TextField(default='')
    vimeo_link = models.TextField(default='')
    other_link = models.TextField(default='')
    portal_link = models.TextField(default='')
    website = models.TextField(default='')
    phone_number = models.TextField(default='')
    address = models.TextField(default='')
    address2 = models.TextField(default='')
    address3 = models.TextField(default='')
    gym_used = models.TextField(default='')
    gym_used2 = models.TextField(default='')
    gym_used3 = models.TextField(default='')
    reviews = models.IntegerField(default=0)
    number_of_reviews = models.IntegerField(default=0)
    product_reviews = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ManyToManyField(Comments)


class FitnessModalProfile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_image', null=True)
    name = models.TextField(default='')
    about_us = models.TextField(default='')
    brands = models.TextField(default='')
    video_code = models.TextField(default='')
    video_code2 = models.TextField(default='')
    video_code3 = models.TextField(default='')
    video_code4 = models.TextField(default='')
    height = models.TextField(default='')
    weight = models.TextField(default='')
    height_unit = models.TextField(default='')
    weight_unit = models.TextField(default='')
    profile_url = models.TextField(default='')
    age = models.TextField(default='')
    compensation = models.TextField(default='')
    c = models.TextField(default='')
    experience = models.TextField(default='')
    languages = models.TextField(default='')
    body_type = models.TextField(default='')
    ethnicity = models.TextField(default='')
    tattoos = models.TextField(default='')
    skin_tone = models.TextField(default='')
    eye_color = models.TextField(default='')
    interested_in = models.TextField(default='')
    modeling_interests = models.TextField(default='')
    piercing = models.TextField(default='')
    hair_length = models.TextField(default='')
    # 0 for not selected
    # 1 for yes
    # 2 for no
    working_with_media = models.IntegerField(default=0)
    facebook = models.TextField(default='')
    instagram = models.TextField(default='')
    youtube = models.TextField(default='')
    twitter = models.TextField(default='')
    blog_link = models.TextField(default='')
    booking_link = models.TextField(default='')
    portal_link = models.TextField(default='')
    vimeo_link = models.TextField(default='')
    other_link = models.TextField(default='')
    website = models.TextField(default='')
    phone_number = models.TextField(default='')
    address = models.TextField(default='')
    address2 = models.TextField(default='')
    address3 = models.TextField(default='')
    gym_used = models.TextField(default='')
    gym_used2 = models.TextField(default='')
    gym_used3 = models.TextField(default='')
    reviews = models.IntegerField(default=0)
    number_of_reviews = models.IntegerField(default=0)
    product_reviews = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ManyToManyField(Comments)


class FitnessCenterRatingInput(models.Model):
    user = models.ForeignKey(FitnessCenterProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)


class FitnessModalRatingInput(models.Model):
    user = models.ForeignKey(FitnessModalProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)


class FitnessProfessionalRatingInput(models.Model):
    user = models.ForeignKey(FitnessProfessionalProfile,
                             on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)


class FitnessCenterProfileSuccessStories(models.Model):
    user = models.ForeignKey(FitnessCenterProfile, on_delete=models.CASCADE)
    story = models.ForeignKey(SuccessStories, on_delete=models.CASCADE)
    is_remove = models.BooleanField(default=False)


class FitnessModalProfileSuccessStories(models.Model):
    user = models.ForeignKey(FitnessModalProfile, on_delete=models.CASCADE)
    story = models.ForeignKey(SuccessStories, on_delete=models.CASCADE)
    is_remove = models.BooleanField(default=False)


class FitnessProfessionalProfileSuccessStories(models.Model):
    user = models.ForeignKey(FitnessProfessionalProfile,
                             on_delete=models.CASCADE)
    story = models.ForeignKey(SuccessStories, on_delete=models.CASCADE)
    is_remove = models.BooleanField(default=False)


class FitnessCenterProfileAdsInformation(models.Model):
    user = models.ForeignKey(FitnessCenterProfile, on_delete=models.CASCADE)
    ad_info = models.ForeignKey(AdsInformation, on_delete=models.CASCADE)
    is_remove = models.BooleanField(default=False)


class FitnessModalProfileAdsInformation(models.Model):
    user = models.ForeignKey(FitnessModalProfile, on_delete=models.CASCADE)
    ad_info = models.ForeignKey(AdsInformation, on_delete=models.CASCADE)
    is_remove = models.BooleanField(default=False)


class FitnessProfessionalAdsInformation(models.Model):
    user = models.ForeignKey(FitnessProfessionalProfile,
                             on_delete=models.CASCADE)
    ad_info = models.ForeignKey(AdsInformation, on_delete=models.CASCADE)
    is_remove = models.BooleanField(default=False)


class FitnessCenterSponsors(models.Model):
    center = models.ForeignKey(FitnessCenterProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fitness_center')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class FitnessCenterPros(models.Model):
    center = models.ForeignKey(FitnessCenterProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fitness_center')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class FitnessCenterGallery(models.Model):
    center = models.ForeignKey(FitnessCenterProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fitness_center')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class FitnessProfessionalsGallery(models.Model):
    center = models.ForeignKey(
        FitnessProfessionalProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fitness_center')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Professional_Sponsers(models.Model):
    center = models.ForeignKey(
        FitnessProfessionalProfile, on_delete=models.CASCADE)
    sponser_name = models.TextField(default='')
    image = models.ImageField(upload_to='fitness_center')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class FitnessModalGallery(models.Model):
    center = models.ForeignKey(FitnessModalProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fitness_center')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)




class Heart_Modal(models.Model):
    user = models.IntegerField(default=0)
    hearts_counter = models.IntegerField(default=0)
    user_session = models.IntegerField(default=0)

class Blog_Heart_Modal(models.Model):
    blog_id = models.IntegerField(default=0)
    hearts_counter = models.IntegerField(default=0)


#Video Links

class FitnessProfessionalYoutubeVideoLinks(models.Model):
    user = models.ForeignKey(FitnessProfessionalProfile,
                             on_delete=models.CASCADE)
    video_link = models.TextField(default='')
    category = models.TextField(default='')

class FitnessModelYoutubeVideoLinks(models.Model):
    user = models.ForeignKey(FitnessModalProfile,
                             on_delete=models.CASCADE)
    video_link = models.TextField(default='')
    category = models.TextField(default='')

class FitnessCenterYoutubeVideoLinks(models.Model):
    user = models.ForeignKey(FitnessCenterProfile,
                             on_delete=models.CASCADE)
    video_link = models.TextField(default='')
    category = models.TextField(default='')