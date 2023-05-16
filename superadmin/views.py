from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as login_auth
from client.models import UserProfile, UserRoles
from django.contrib.auth.models import User
from client.utils import get_all_unique_time_zones
from .models import *
import json
from client.constants import *
from client.models import FitnessProfessionalProfile, FitnessModalProfile, FitnessCenterProfile
from django.http import HttpResponse
import googlemaps


def login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['username'] if 'username' in request.POST else ''
        password = request.POST['password'] if 'password' in request.POST else ''
        email = email.lower().strip()
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                if user.is_superuser:
                    login_auth(request, user)
                    return redirect('superadmin:users_listing')
        context = {'error': 'Email or Password is wrong'}
    return render(request, 'superadmin/login.html', context=context)


@login_required
def users_listing(request):
    users_info = UserProfile.objects.all().order_by('-id')
    time_zones = get_all_unique_time_zones()
    user_roles = UserRoles.objects.all()
    context = {'time_zones': time_zones,
               'user_roles': user_roles, 'users_info': users_info}

    return render(request, 'superadmin/user_listing.html', context=context)


@login_required
def searchuser(request):
    search = request.POST['search']
    role = request.POST.get('user')

    if role != None and search != "":
        if role == "professional":
            users_info = UserProfile.objects.filter(
                roles__name="Fitness Professional", user__username__icontains=search)
            time_zones = get_all_unique_time_zones()
            user_roles = UserRoles.objects.all()
            context = {'time_zones': time_zones,
                       'user_roles': user_roles, 'users_info': users_info}
            return render(request, 'superadmin/user_listing.html', context=context)
        elif role == "model":
            users_info = UserProfile.objects.filter(
                roles__name="Fitness Model", user__username__icontains=search)
            time_zones = get_all_unique_time_zones()
            user_roles = UserRoles.objects.all()
            context = {'time_zones': time_zones,
                       'user_roles': user_roles, 'users_info': users_info}
            return render(request, 'superadmin/user_listing.html', context=context)
        else:
            users_info = UserProfile.objects.filter(
                roles__name="Fitness Center", user__username__icontains=search)
            time_zones = get_all_unique_time_zones()
            user_roles = UserRoles.objects.all()
            context = {'time_zones': time_zones,
                       'user_roles': user_roles, 'users_info': users_info}
            return render(request, 'superadmin/user_listing.html', context=context)
    elif search != "":
        users_info = UserProfile.objects.filter(
            user__username__icontains=search)
        time_zones = get_all_unique_time_zones()
        user_roles = UserRoles.objects.all()
        context = {'time_zones': time_zones,
                   'user_roles': user_roles, 'users_info': users_info}
        return render(request, 'superadmin/user_listing.html', context=context)
    elif role != None:
        if role == "professional":
            users_info = UserProfile.objects.filter(
                roles__name="Fitness Professional")
            time_zones = get_all_unique_time_zones()
            user_roles = UserRoles.objects.all()
            context = {'time_zones': time_zones,
                       'user_roles': user_roles, 'users_info': users_info}
            return render(request, 'superadmin/user_listing.html', context=context)
        elif role == "model":
            users_info = UserProfile.objects.filter(
                roles__name="Fitness Model")
            time_zones = get_all_unique_time_zones()
            user_roles = UserRoles.objects.all()
            context = {'time_zones': time_zones,
                       'user_roles': user_roles, 'users_info': users_info}
            return render(request, 'superadmin/user_listing.html', context=context)
        else:
            users_info = UserProfile.objects.filter(
                roles__name="Fitness Center")
            time_zones = get_all_unique_time_zones()
            user_roles = UserRoles.objects.all()
            context = {'time_zones': time_zones,
                       'user_roles': user_roles, 'users_info': users_info}
            return render(request, 'superadmin/user_listing.html', context=context)
    users_info = UserProfile.objects.all()
    time_zones = get_all_unique_time_zones()
    user_roles = UserRoles.objects.all()
    context = {'time_zones': time_zones,
               'user_roles': user_roles, 'users_info': users_info}
    return render(request, 'superadmin/user_listing.html', context=context)


@login_required
def change_activeness_user(request):
    data = json.loads(request.body.decode('utf-8'))
    id_ = data['id']
    check = data['check']

    up_ = UserProfile.objects.filter(id=int(id_)).last()
    if up_:
        user = up_.user
        user.is_active = check
        user.save()

    return JsonResponse(data={'success': True}, safe=False)


@login_required
def delete_user(request, id, role, role_id):
    userProfile = UserProfile.objects.get(id=id)
    # user_ = User.objects.get(email=userProfile.user.email)

    if role == "Fitness Professional":
        userRole = UserRoles.objects.get(id=role_id)
        userProfile.roles.remove(userRole)
        userProfile.save()
        user_pro_ = FitnessProfessionalProfile.objects.get(user=userProfile)
        user_pro_.delete()
        FitnessProfessionalProfile.objects.create(user=userProfile)
        
    
    if role == "Fitness Center":
        # userCenter = FitnessCenterProfile.objects.get(user=userProfile)
        # userCenter.delete()
        userRole = UserRoles.objects.get(id=role_id)
        userProfile.roles.remove(userRole)
        userProfile.save()
        user_center_ = FitnessCenterProfile.objects.get(user=userProfile)
        user_center_.delete()
        FitnessCenterProfile.objects.create(user=userProfile)

    if role == "Fitness Model":
        # userModel = FitnessModalProfile.objects.get(user=userProfile)
        # userModel.delete()
        userRole = UserRoles.objects.get(id=role_id)
        userProfile.roles.remove(userRole)
        userProfile.save()
        user_model_ = FitnessModalProfile.objects.get(user=userProfile)
        user_model_.delete()
        FitnessModalProfile.objects.create(user=userProfile)
    return redirect("superadmin:users_listing")


@login_required
def ambassadors_listing(request):
    if request.method == 'POST':

        id_ = request.POST['id'] if 'id' in request.POST else None

        name = request.POST['name']

        tagline = request.POST['tagline']
        profile_image = request.FILES['profile_avatar'] if 'profile_avatar' in request.FILES else None

        instagram = request.POST['instagram'] if 'instagram' in request.POST else ''
        youtube = request.POST['youtube'] if 'youtube' in request.POST else ''
        facebook = request.POST['facebook'] if 'facebook' in request.POST else ''
        twitter = request.POST['twitter'] if 'twitter' in request.POST else ''
        description = request.POST['description'] if 'description' in request.POST else ''

        if id_:
            ambs = AmbassadorsInfo.objects.get(id=int(id_))
            ambs.name = name
            ambs.tagline = tagline
            ambs.description = description

            if profile_image:
                ambs.profile_image = profile_image
            ambs.save()

        else:
            ambs = AmbassadorsInfo.objects.create(
                name=name, tagline=tagline, profile_image=profile_image, description = description)

        ambs.instagram = instagram
        ambs.youtube = youtube
        ambs.twitter = twitter
        ambs.facebook = facebook
        ambs.save()

    ambassadors = AmbassadorsInfo.objects.all().order_by('-id')
    context = {'ambassadors': ambassadors}
    return render(request, 'superadmin/ambassadors_listing.html', context=context)


@login_required
def delete_ambassador(request):
    data = json.loads(request.body.decode('utf-8'))
    data = data['id'] if 'id' in data else None
    if data:
        AmbassadorsInfo.objects.filter(id=int(data)).delete()
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def change_activeness_ambassador(request):
    data = json.loads(request.body.decode('utf-8'))
    id_ = data['id']
    check = data['check']

    if check:
        check = False
    else:
        check = True

    AmbassadorsInfo.objects.filter(id=int(id_)).update(is_remove=check)
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def change_activeness_collaborators(request):
    data = json.loads(request.body.decode('utf-8'))
    id_ = data['id']
    check = data['check']

    if check:
        check = False
    else:
        check = True

    CollaboratorsInfo.objects.filter(id=int(id_)).update(is_remove=check)
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def change_activeness_sponsor(request):
    data = json.loads(request.body.decode('utf-8'))
    id_ = data['id']
    check = data['check']

    if check:
        check = False
    else:
        check = True

    SponsorsInfo.objects.filter(id=int(id_)).update(is_remove=check)
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def change_activeness_blog(request):
    data = json.loads(request.body.decode('utf-8'))
    id_ = data['id']
    check = data['check']

    if check:
        check = False
    else:
        check = True

    Blog.objects.filter(id=int(id_)).update(is_remove=check)
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def sponsors_listing(request):
    if request.method == 'POST':
        id_ = request.POST['id'] if 'id' in request.POST else None
        profile_avatar = request.FILES['profile_avatar'] if 'profile_avatar' in request.FILES else None

        if id_:
            spo = SponsorsInfo.objects.get(id=int(id_))
            spo.profile_image = profile_avatar
            spo.save()
        else:
            SponsorsInfo.objects.create(profile_image=profile_avatar)

    sponsors = SponsorsInfo.objects.all().order_by('-id')
    context = {'sponsors': sponsors}
    return render(request, 'superadmin/sponsors_listing.html', context=context)


@login_required
def delete_sponsor(request):
    data = json.loads(request.body.decode('utf-8'))
    data = data['id'] if 'id' in data else None
    if data:
        SponsorsInfo.objects.filter(id=int(data)).delete()
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def delete_blog(request):
    data = json.loads(request.body.decode('utf-8'))
    data = data['id'] if 'id' in data else None
    if data:
        Blog.objects.filter(id=int(data)).delete()
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def delete_collaborator(request):
    data = json.loads(request.body.decode('utf-8'))
    data = data['id'] if 'id' in data else None
    if data:
        CollaboratorsInfo.objects.filter(id=int(data)).delete()
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def collaborators_listing(request):
    if request.method == 'POST':
        id_ = request.POST['id'] if 'id' in request.POST else None
        profile_avatar = request.FILES['profile_avatar'] if 'profile_avatar' in request.FILES else None
        title = request.POST['title']
        sub_title = request.POST['sub_title']
        instagram = request.POST['instagram'] if 'instagram' in request.POST else ''
        youtube = request.POST['youtube'] if 'youtube' in request.POST else ''
        facebook = request.POST['facebook'] if 'facebook' in request.POST else ''
        twitter = request.POST['twitter'] if 'twitter' in request.POST else ''

        if id_:
            ci = CollaboratorsInfo.objects.get(id=int(id_))
            if profile_avatar:
                ci.profile_image = profile_avatar
        else:
            ci = CollaboratorsInfo.objects.create(profile_image=profile_avatar)

        ci.title = title
        ci.sub_title = sub_title
        ci.instagram = instagram
        ci.youtube = youtube
        ci.twitter = twitter
        ci.facebook = facebook
        ci.save()

    collaborators = CollaboratorsInfo.objects.all().order_by('-id')
    context = {'collaborators': collaborators}
    return render(request, 'superadmin/collaborators_listing.html', context=context)


@login_required
def blog_listing(request):
    BlogCategories.objects.get_or_create(slug='nutrition', name='Nutrition')
    BlogCategories.objects.get_or_create(slug='recipes', name='Recipies')
    BlogCategories.objects.get_or_create(slug='workout', name='Workouts')
    BlogCategories.objects.get_or_create(slug='reviews', name='Reviews')
    BlogCategories.objects.get_or_create(slug='news', name='News')
    BlogCategories.objects.get_or_create(slug='music', name='Music')

    if request.method == 'POST':
        author_image = request.FILES['author_image'] if 'author_image' in request.FILES else None
        featured_image = request.FILES['featured_image'] if 'featured_image' in request.FILES else None
        second_featured_image = request.FILES['second_featured_image'] if 'second_featured_image' in request.FILES else None
        category = request.POST['category']
        author_name = request.POST['author_name']
        tagline = request.POST['tagline']
        details = request.POST['details']
        title = request.POST['title']
        video = request.POST['video']

        id_ = request.POST['id'] if 'id' in request.POST else None
        category = BlogCategories.objects.get(id=int(category))

        if id_:
            blog_ = Blog.objects.get(id=int(id_))
            blog_.category = category
            blog_.author = author_name
            blog_.title = title
            blog_.short_description = tagline
            blog_.details = details
            blog_.video_link = video

            sfiv = request.POST['second_featured_image_value']
            if not sfiv:
                blog_.second_featured_image = None

            if featured_image:
                blog_.featured_image = featured_image
            if second_featured_image:
                blog_.second_featured_image = second_featured_image
            if author_image:
                blog_.author_profile_pic = author_image
            blog_.save()

        else:
            bl_ = Blog.objects.create(title=title, featured_image=featured_image, video_link=video,
                                      author=author_name, author_profile_pic=author_image,
                                      short_description=tagline, details=details,
                                      is_remove=False,
                                      category=category)
            if second_featured_image:
                bl_.second_featured_image = second_featured_image
                bl_.save()

    blogs = Blog.objects.all().order_by('-id')
    categories = BlogCategories.objects.all()
    context = {'blogs': blogs, 'categories': categories}
    return render(request, 'superadmin/blog_listing.html', context=context)


@login_required
def landing_page(request):
    if request.method == 'POST':
        banner_text = request.POST['banner_text']
        about_us_text = request.POST['about_us_text']
        main_heading = request.POST['main_heading']
        sub_heading = request.POST['sub_heading']
        footer_about_section = request.POST['footer_about_section']
        footer_phone_no = request.POST['footer_phone_no']
        terms_and_conditionss = request.POST['terms_and_conditionss']
        privacy_policy = request.POST['privacy_policy']

        instagram = request.POST['instagram'] if 'instagram' in request.POST else ''
        youtube = request.POST['youtube'] if 'youtube' in request.POST else ''
        facebook = request.POST['facebook'] if 'facebook' in request.POST else ''
        twitter = request.POST['twitter'] if 'twitter' in request.POST else ''
        linkedin = request.POST['linkedin'] if 'linkedin' in request.POST else ''

        print(request.POST)

        banner = request.FILES['banner'] if 'banner' in request.FILES else ''
        about_us_landing = request.FILES['about_us_landing'] if 'about_us_landing' in request.FILES else ''

        landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
        landing_page_.banner_text = banner_text
        landing_page_.about_us_text = about_us_text
        landing_page_.main_heading = main_heading
        landing_page_.sub_heading = sub_heading
        landing_page_.footer_about_section = footer_about_section
        landing_page_.footer_phone_no = footer_phone_no
        landing_page_.privacy_policy = privacy_policy
        landing_page_.terms_and_conditionss = terms_and_conditionss

        landing_page_.instagram = instagram
        landing_page_.youtube = youtube
        landing_page_.facebook = facebook
        landing_page_.twitter = twitter
        landing_page_.linkedin = linkedin

        if banner:
            landing_page_.banner = banner
        if about_us_landing:
            landing_page_.about_us_landing = about_us_landing

        landing_page_.save()

    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    context = {'landing_page': landing_page_}
    return render(request, 'superadmin/landing_page.html', context=context)


@login_required
def create_user(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    username = data['username']
    password = data['password']
    role = data['userrole']
    timezone = data
    city, country, state = "", "", ""
    gmaps_key = googlemaps.Client(
        key="AIzaSyCy7x2Sx_u2gBDfSBfksctKjknIHpAqy24")
    geocode_result3 = gmaps_key.geocode(timezone)
    address_components = geocode_result3[0]['address_components']
    for obj in address_components:
        if obj['types']:
            if obj['types'][0] == 'locality':
                city = obj['long_name']
            if obj['types'][0] == 'country':
                country = obj['long_name']
            if obj['types'][0] == 'administrative_area_level_1':
                state = obj['long_name']

    user, created = User.objects.get_or_create(username=email, email=email)
    if not created:
        return JsonResponse(data={'success': False}, safe=False)

    user.set_password(password)
    user.first_name = username
    user.save()

    role_ = UserRoles.objects.get(id=int(role))

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.username = username
    user_profile.sign_up_role = role_
    user_profile.active_user_role = role_
    user_profile.country = country
    user_profile.city = city
    user_profile.state = state
    user_profile.roles.add(role_)
    user_profile.save()

    if role_.name == FITNESS_MODAL:
        FitnessModalProfile.objects.get_or_create(user=user_profile)
    if role_.name == FITNESS_PROFESSIONAL:
        FitnessProfessionalProfile.objects.get_or_create(user=user_profile)
    if role_.name == FITNESS_CENTER:
        FitnessCenterProfile.objects.get_or_create(user=user_profile)

    return JsonResponse(data={'success': True}, safe=True)
