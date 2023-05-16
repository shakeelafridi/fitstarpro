from random import shuffle
from .models import *
from .constants import GOOGLE_API_KEY
import pytz
import json
import folium
import googlemaps


def get_all_unique_time_zones():
    all_tz = []
    for index, tz in enumerate(pytz.all_timezones):
        tz_name = pytz.timezone(tz)
        try:
            get_city_name = str(tz).split('/')
            all_tz.append(
                {'city': str(get_city_name[1]), 'value': str(tz_name)})
        except Exception as e:
            pass
    return all_tz


def get_all_user_roles():
    all_tz = []
    for index, tz in enumerate(pytz.all_timezones):
        tz_name = pytz.timezone(tz)
        try:
            get_city_name = str(tz).split('/')
            all_tz.append(
                {'city': str(get_city_name[1]), 'value': str(tz_name)})
        except Exception as e:
            print(e)
    return all_tz


def get_generic_information(user):
    dict_ = {
        'name': user.username,
        'dob': user.date_of_birth,
        'time_zone_info': user.time_zone_info
    }


def get_success_obj(obj):
    obj = obj.story
    return {
        'before': str(obj.before.url),
        'after': str(obj.after.url),
        'description': obj.description,
        'instagram_link': obj.instagram_link,
        'id': obj.id
    }


def get_success_stories(success_stories):
    success_stories_ = []
    for obj in success_stories:
        success_stories_.append(get_success_obj(obj))

    if success_stories.count() == 1:
        success_stories_.append(get_success_obj(success_stories[0]))
        success_stories_.append(get_success_obj(success_stories[0]))
    if success_stories.count() == 2:
        success_stories_.append(get_success_obj(success_stories[1]))
        success_stories_.append(get_success_obj(success_stories[0]))
        success_stories_.append(get_success_obj(success_stories[1]))
        success_stories_.append(get_success_obj(success_stories[0]))
    return success_stories_


def get_fitness_professional_profile(user):
    fcp = FitnessProfessionalProfile.objects.get(user=user)

    success_stories = FitnessProfessionalProfileSuccessStories.objects.filter(
        is_remove=False, user=fcp).order_by('?')
    gallery = FitnessProfessionalsGallery.objects.filter(
        is_remove=False, center=fcp).order_by('?')

    sponsers = Professional_Sponsers.objects.filter(
        is_remove=False, center=fcp).order_by('?')
    print(sponsers, '-----------------------sponser')
    ads_info = FitnessProfessionalAdsInformation.objects.filter(
        is_remove=False, user=fcp).order_by('?')

    try:
        youtube_links_list=[]
        youtube_links_ = FitnessProfessionalYoutubeVideoLinks.objects.filter(user=fcp)
        for obj in youtube_links_:
            youtube_links_dict_ = {"id":obj.id,"video_link": obj.video_link, "video_category":obj.category}
            youtube_links_list.append(youtube_links_dict_)
    except:
        pass

    languages_list = fcp.languages.split(",")
    languages_list = [x.strip() for x in languages_list]
    specialities_list = fcp.specialities.split(",")
    specialities_list = [x.strip() for x in specialities_list]
    certification_list = fcp.certifications.split(",")
    certification_list = [x.strip() for x in certification_list]
    activities_list = fcp.activities.split(",")
    activities_list = [x.strip() for x in activities_list]
    try:
        product_reviews = json.loads(fcp.product_reviews)
    except:
        product_reviews = []
    try:
        fitness_awards = json.loads(fcp.fitness_awards)
    except:
        fitness_awards = []

    dict_ = {
        'profile': fcp,
        'languages_list': languages_list,
        'specialities_list': specialities_list,
        'certification_list': certification_list,
        'fitness_awards': fitness_awards,
        'activities_list': activities_list,
        'product_reviews': product_reviews,
        'user': user,
        'user_id' : user.id,
        'success_stories': get_success_stories(success_stories),
        'gallery': gallery,
        'ads_info': ads_info,
        'sponsers': sponsers,
        'youtube_links':youtube_links_list,
        'gender':user.gender

    }
    return dict_


def get_fitness_center_profile(user):
    fcp = FitnessCenterProfile.objects.get(user=user)
    fitness_center_type = FitnessCenterType.objects.all()

    try:
        youtube_links_list=[]
        youtube_links_ = FitnessCenterYoutubeVideoLinks.objects.filter(user=fcp)
        for obj in youtube_links_:
            youtube_links_dict_ = {"id":obj.id,"video_link": obj.video_link,"video_category":obj.category}
            youtube_links_list.append(youtube_links_dict_)
    except:
        pass

    success_stories = FitnessCenterProfileSuccessStories.objects.filter(
        is_remove=False, user=fcp).order_by('?')
    gallery = FitnessCenterGallery.objects.filter(
        is_remove=False, center=fcp).order_by('?')
    pros = FitnessCenterPros.objects.filter(
        is_remove=False, center=fcp).order_by('?')
    ads_info = FitnessCenterProfileAdsInformation.objects.filter(
        is_remove=False, user=fcp).order_by('?')
    specialities_list = fcp.specialities.split(",")
    specialities_list = [x.strip() for x in specialities_list]
    languages_list = fcp.languages.split(",")
    languages_list = [x.strip() for x in languages_list]
    fitness_pros_list = fcp.fitness_pros.all()
    fitness_pros_list = [x.id for x in fitness_pros_list]
    try:
        product_reviews = json.loads(fcp.product_reviews)
    except:
        product_reviews = []

    dict_ = {
        'profile': fcp,
        'product_reviews': product_reviews,
        'languages_list': languages_list,
        'fitness_pros_list': fitness_pros_list,
        'specialities_list': specialities_list,
        'user': user,
        'success_stories': get_success_stories(success_stories),
        'fitness_center_type': fitness_center_type,
        'gallery': gallery,
        'pros': pros,
        'ads_info': ads_info,
        'youtube_links':youtube_links_list
    }
    return dict_


def get_fitness_modal_profile(user):
    fcp = FitnessModalProfile.objects.get(user=user)

    try:
        youtube_links_list=[]
        youtube_links_ = FitnessModelYoutubeVideoLinks.objects.filter(user=fcp)
        for obj in youtube_links_:
            youtube_links_dict_ = {"id":obj.id,"video_link": obj.video_link,"video_category":obj.category}
            youtube_links_list.append(youtube_links_dict_)
    except:
        pass

    success_stories = FitnessModalProfileSuccessStories.objects.filter(
        is_remove=False, user=fcp).order_by('?')
    gallery = FitnessModalGallery.objects.filter(
        is_remove=False, center=fcp).order_by('?')
    ads_info = FitnessModalProfileAdsInformation.objects.filter(
        is_remove=False, user=fcp).order_by('?')

    languages_list = fcp.languages.split(",")
    languages_list = [x.strip() for x in languages_list]
    interested_in_list = fcp.interested_in.split(",")
    interested_in_list = [x.strip() for x in interested_in_list]
    modeling_interests_list = fcp.modeling_interests.split(",")
    modeling_interests_list = [x.strip() for x in modeling_interests_list]
    try:
        product_reviews = json.loads(fcp.product_reviews)
    except:
        product_reviews = []

    dict_ = {
        'profile': fcp,
        'product_reviews': product_reviews,
        'languages_list': languages_list,
        'interested_in_list': interested_in_list,
        'modeling_interests_list': modeling_interests_list,
        'user': user,
        'success_stories': get_success_stories(success_stories),
        'gallery': gallery,
        'ads_info': ads_info,
        'youtube_links':youtube_links_list,
        'gender':user.gender
    }
    return dict_


def get_top_fitness_center():
    top_fitness_cent = FitnessCenterProfile.objects.filter(
        user__user__is_active=True).order_by('?')[:3]
    final_list = []
    for obj in top_fitness_cent:
        profile_img = ''
        if obj.profile_image:
            profile_img = str(obj.profile_image.url)

        name = obj.user.user.first_name
        if obj.name:
            name = obj.name

        profile_url = obj.id
        if obj.profile_url:
            profile_url = obj.profile_url

        url = '/center/' + str(profile_url)

        final_list.append(
            {'profile_image': profile_img, 'name': name, 'url': url})
    shuffle(final_list)
    return final_list


def get_top_fitness_model():
    top_fitness_mod = FitnessModalProfile.objects.filter(
        user__user__is_active=True).order_by('?')[:3]
    final_list = []
    for obj in top_fitness_mod:
        profile_img = ''
        if obj.profile_image:
            profile_img = str(obj.profile_image.url)

        name = obj.user.user.first_name
        if obj.name:
            name = obj.name

        profile_url = obj.id
        if obj.profile_url:
            profile_url = obj.profile_url

        url = '/model/' + str(profile_url)
        final_list.append(
            {'profile_image': profile_img, 'name': name, 'url': url})
    shuffle(final_list)
    return final_list


def get_top_fitness_pros():
    top_fitness_pros = FitnessProfessionalProfile.objects.filter(
        user__user__is_active=True).order_by('?')[:3]
    final_list = []

    for obj in top_fitness_pros:
        profile_img = ''
        if obj.profile_image:
            profile_img = str(obj.profile_image.url)

        name = obj.user.user.first_name
        if obj.name:
            name = obj.name

        profile_url = obj.id
        if obj.profile_url:
            profile_url = obj.profile_url

        url = '/pro/' + str(profile_url)

        final_list.append(
            {'profile_image': profile_img, 'name': name, 'url': url})

    shuffle(final_list)
    return final_list


def get_map_object(profile_):
    gmaps_key = googlemaps.Client(key=GOOGLE_API_KEY)
    address = profile_['profile'].address
    address2 = profile_['profile'].address2
    address3 = profile_['profile'].address3
    m = ""
    lng2 = ""
    lat2 = ""
    lng3 = ""
    lat3 = ""
    if address != "":
        try:
            geocode_result = gmaps_key.geocode(address)
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lng = geocode_result[0]["geometry"]["location"]["lng"]
            m = folium.Map(width=840, height=485, location=[lat, lng])
            folium.Marker([lat, lng], tooltip=address,
                          icon=folium.Icon(color='#ff1a1a'), zoom_start=9, zoom_control=True).add_to(m)
            # folium.TileLayer(
            #     tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            #     attr='Google',
            #     name='Google Satellite',
            #     overlay=True,
            #     control=True
            # ).add_to(m)
            folium.TileLayer(
                tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                attr='Google',
                name='Google Maps',
                overlay=True,
                control=True
            ).add_to(m)
            # folium.TileLayer(
            #     tiles='https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
            #     attr='Google',
            #     name='Google Terrain',
            #     overlay=True,
            #     control=True
            # ).add_to(m)
            # folium.TileLayer(
            #     tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            #     attr='Google',
            #     name='Google Satellite',
            #     overlay=True,
            #     control=True
            # ).add_to(m)
            # folium.TileLayer(
            #     tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            #     attr='Esri',
            #     name='Esri Satellite',
            #     overlay=True,
            #     control=True
            # ).add_to(m)
            # folium.TileLayer('Stamen Terrain').add_to(m)
            # folium.TileLayer('Stamen Toner').add_to(m)
            # folium.TileLayer('Stamen Water Color').add_to(m)
            # folium.TileLayer('cartodbpositron').add_to(m)
            # folium.TileLayer('cartodbdark_matter').add_to(m)
            folium.LayerControl().add_to(m)
        except Exception as e:
            pass

        if address2 != "":
            try:
                geocode_result2 = gmaps_key.geocode(address2)
                lat2 = geocode_result2[0]["geometry"]["location"]["lat"]
                lng2 = geocode_result2[0]["geometry"]["location"]["lng"]
                folium.Marker([lat2, lng2], tooltip=address2,
                              icon=folium.Icon(color='orange')).add_to(m)
            except Exception as e:
                pass

        if address3 != "":
            try:
                geocode_result3 = gmaps_key.geocode(address3)
                lat3 = geocode_result3[0]["geometry"]["location"]["lat"]
                lng3 = geocode_result3[0]["geometry"]["location"]["lng"]
                folium.Marker([lat3, lng3], tooltip=address3,
                              icon=folium.Icon(color='green')).add_to(m)
            except Exception as e:
                pass
        try:
            m = m._repr_html_()
        except Exception as e:
            m = ""
    return m


def get_city_and_country_from_geo_value(value):
    city, country, state = "", "", ""
    gmaps_key = googlemaps.Client(key=GOOGLE_API_KEY)
    try:
        geocode_result3 = gmaps_key.geocode(value)
        address_components = geocode_result3[0]['address_components']
        for obj in address_components:
            if obj['types']:
                if obj['types'][0] == 'locality':
                    city = obj['long_name']
                if obj['types'][0] == 'country':
                    country = obj['long_name']
                if obj['types'][0] == 'administrative_area_level_1':
                    state = obj['long_name']
    except Exception as e:
        print(e)
    return city, country, state
