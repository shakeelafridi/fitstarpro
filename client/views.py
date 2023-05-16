from django.db.models import Avg
from random import shuffle
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from .utils import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
from superadmin.models import *
from .constants import *
from django.contrib.messages import get_messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
import json
import requests
import re

from random import randint
from client.models import Heart_Modal
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError
active = ""

def password_reset_request(request):
    message = ''
    if request.method == "POST":
        domain = request.headers['Host']
        try:
            data = request.POST['email']
        except:
            message = 'invalid email'
        domain = 'fitstar.pro'
        associated_users = User.objects.filter(Q(email=data))
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "client/accounts/password_reset_text_email_context.txt"
                c = {
                    "email": user.email,
                    'domain': domain,
                    'site_name': 'Interface',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'fitstar@fitstar.pro',
                              [user.email], fail_silently=False)
                except Exception as e:
                    return render(request, 'client/accounts/forgot_password.html', {"message":"Invalid email"})

                return redirect("client:forgot_password_done")
        else:
            message = 'Invalid email'
    return render(request, 'client/accounts/forgot_password.html',{'message':message})


def login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login_auth(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Email/Password is wrong')
    return render(request, 'client/accounts/login.html')


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            match = User.objects.get(username=email)
        except:
            return render(request, 'client/accounts/forgot_password.html', {'message':"invalid email"})
    password_reset_request(request)


def logout(request):
    logout_auth(request)
    return redirect('/')


def register(request):
    time_zones = TimeZone.objects.all()
    countries = Countries.objects.all()
    user_roles = UserRoles.objects.all()
    users = UserProfile.objects.all()

    context = {'countries': countries,
               'time_zones': time_zones, 'user_roles': user_roles,
               "users": users}

    if request.method == 'POST':
        data = request.POST
        clientkey = data['g-recaptcha-response']
        secretkey = '6LdL8AUaAAAAAJdaLb7e4cKu-eCy2qQshTekE6tl'
        captchadata = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=captchadata)
        response = json.loads(r.text)
        verify = response['success']
        if verify:
            username = data['username']
            email = data['email'].lower().strip()
            password = data['password']
            confirm_password = data['c_password']
            # country = data['country']
            # city = data['city']
            role = data['role'] if 'role' in data else None
            gender = data['gender'] if 'gender' in data else None
            location = data['location']
            # timezone = data['timezone']

            if not role:
                messages.info(request, 'Select Role to complete registration')
                return render(request, 'client/accounts/signup.html', context=context)

            # if not gender:
            #     messages.info(
            #         request, 'Select Gender to complete registration')
            #     return render(request, 'client/accounts/signup.html', context=context)

            city, country, state = get_city_and_country_from_geo_value(
                location)

            if password != confirm_password:
                messages.error(
                    request, 'Password & Confirm Password Must Be Same')
                return render(request, 'client/accounts/signup.html', context=context)

            if not email:
                messages.error(request, 'Email is required')
                return render(request, 'client/accounts/signup.html', context=context)

            if not role:
                messages.error(request, 'Please select role')
                return render(request, 'client/accounts/signup.html', context=context)

            # if not timezone:
            #     messages.error(request, 'Please select timezone')
            #     return render(request, 'client/accounts/signup.html', context=context)

            user, created = User.objects.get_or_create(
                username=email, email=email)
            if not created:
                messages.error(
                    request, 'This email address is already registered')
                return render(request, 'client/accounts/signup.html', context=context)

            user.set_password(password)
            user.first_name = username
            user.save()

            role_ = UserRoles.objects.get(id=int(role))

            user_profile, created = UserProfile.objects.get_or_create(
                user=user)
            user_profile.username = username
            # user_profile.time_zone_info = timezone
            user_profile.location = location
            user_profile.country = country
            user_profile.city = city
            user_profile.state = state
            user_profile.referred = gender
            user_profile.sign_up_role = role_
            user_profile.active_user_role = role_

            user_profile.roles.add(role_)
            user_profile.save()

            if role_.name == FITNESS_MODAL:
                FitnessModalProfile.objects.get_or_create(user=user_profile)
            if role_.name == FITNESS_PROFESSIONAL:
                FitnessProfessionalProfile.objects.get_or_create(
                    user=user_profile)
            if role_.name == FITNESS_CENTER:
                FitnessCenterProfile.objects.get_or_create(user=user_profile)

            login_auth(request, user)
            messages.info(request, 'Successfully Logged In')
            return redirect('/')
        else:
            messages.info(request, 'Complete reCAPTCHA to signup!')
            return render(request, 'client/accounts/signup.html', context=context)

    return render(request, 'client/accounts/signup.html', context=context)


def home(request):
    ambassadors = AmbassadorsInfo.objects.filter(is_remove=False).order_by('?')
    sponsors = SponsorsInfo.objects.filter(is_remove=False).order_by('?')
    top_fitness_ = get_top_fitness_pros()
    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)

    #for visitor
    visitor_id = ''
    if not request.session.has_key('visitor_id'):
        for _ in range(8):
            visitor_id += str(randint(1, 9))
        request.session['visitor_id'] = visitor_id

    context = {'ambassadors': ambassadors, 'sponsors': sponsors, 'top_profiles': top_fitness_,
               'landing_page': landing_page_}
    return render(request, 'client/index.html', context=context)


def contact_us(request):
    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    context = {'landing_page': landing_page_}
    if request.method == 'POST':
        clientkey = request.POST.get('g-recaptcha-response')
        secretkey = '6LdL8AUaAAAAAJdaLb7e4cKu-eCy2qQshTekE6tl'
        captchadata = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=captchadata)
        response = json.loads(r.text)
        verify = response['success']
        landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
        name = request.POST.get('name')
        email = request.POST.get('email')
        chat_code = request.POST.get('chat-code')
        print(chat_code,'------------------chat code')
        message = request.POST.get('message')
        if verify:
            try:
                send_mail(name, "Email: " + email + "\nMessage: " + message+chat_code, 'fitstar@fitstar.pro',
                          ['fitstar@fitstar.pro'], fail_silently=False)
                messages.info(request, 'Your message has been sent!')
                print(name, email, message)
            except Exception as e:
                print(e)
            return render(request, 'client/contact-us.html', context=context)
        else:
            messages.info(request, 'Complete reCAPTCHA to send message!')
            return render(request, 'client/contact-us.html', context=context)
    return render(request, 'client/contact-us.html', context=context)


def user_contact_us(request):
    if request.method == "POST":
        url = '/' + '/'.join(request.META['HTTP_REFERER'].split('/')[3:])
        user_email = request.POST['profile_user_email']
        clientkey = request.POST.get('g-recaptcha-response')
        secretkey = '6LdL8AUaAAAAAJdaLb7e4cKu-eCy2qQshTekE6tl'
        captchadata = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=captchadata)
        response = json.loads(r.text)
        verify = response['success']
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        description = request.POST['description']
        if verify:
            try:
                # user_email = "meharbanliaquat@gmail.com"
                send_mail(subject,
                          "This is message from one of our user! \nName: " + name + "\nEmail: " + email + "\nDescription: " +
                          description, 'fitstar@fitstar.pro', [user_email], fail_silently=False)
                messages.info(request, 'Your message has been sent!')
            except Exception as e:
                messages.info(request, 'Please try again!')
            # return redirect('client:profile')
            return HttpResponseRedirect(url)
        else:
            messages.info(request, 'Complete reCAPTCHA to send message!')
            return HttpResponseRedirect(url)
            # return redirect('client:profile')


def privacy_policy(request):
    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    return render(request, 'client/privacy_policy.html', context={'landing_page': landing_page_})


def terms_and_conditions(request):
    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    return render(request, 'client/terms_and_conditions.html', context={'landing_page': landing_page_})


def about_us(request):
    collaborators = CollaboratorsInfo.objects.filter(
        is_remove=False).order_by('?')
    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)

    return render(request, 'client/about-us.html',
                  context={'collaborators': collaborators, 'landing_page': landing_page_})


def blog(request):
    category = request.GET.get('category', 'all')
    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)

    blog = Blog.objects.all()
    is_category = 'all'

    if category == 'all':
        blog = Blog.objects.filter(is_remove=False)
    else:
        bc = BlogCategories.objects.filter(slug=category).last()
        if bc:
            is_category = bc.slug.lower()
            blog = Blog.objects.filter(category=bc, is_remove=False)

    context = {'blog': blog, 'category': is_category,
               'landing_page': landing_page_}
    return render(request, 'client/blogs.html', context=context)


def fitness_pros(request):
    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    specialities = Specialities.objects.all()
    fitness_pro = FitnessProfessionalProfile.objects.filter(
        user__user__is_active=True)

    name = request.GET.get('name', '')
    speciality = request.GET.get('speciality', '')
    location = request.GET.get('location', '')

    if name:
        # fitness_pro = fitness_pro.filter(name__icontains=name)
        fitness_pro = fitness_pro.filter(
            Q(user__username__icontains=name) | Q(name__icontains=name))
    if location:
        # city, country, state = get_city_and_country_from_geo_value(location)
        # fitness_pro = fitness_pro.filter(Q(address__icontains=location) | Q(user__city__icontains=city) |
        #                                 Q(user__country__icontains=country) | Q(user__state__icontains=state))
        fitness_pro = fitness_pro.filter(
            Q(user__location__icontains=location) | Q(address__icontains=location) | Q(address2__icontains=location) | Q(address3__icontains=location))
    if speciality != '0':
        fitness_pro = fitness_pro.filter(specialities__icontains=speciality)

    top_fitness_ = get_top_fitness_pros()

    page = request.GET.get('page', 1)
    paginator = Paginator(fitness_pro, 10)
    try:
        fitness_pro = paginator.page(page)
    except PageNotAnInteger:
        fitness_pro = paginator.page(1)
    except EmptyPage:
        fitness_pro = paginator.page(paginator.num_pages)

    return render(request, 'client/fitness-pros.html',
                  context={'fitness_pros': fitness_pro, 'top_fitness': top_fitness_,
                           'name': name, 'location': location, 'speciality': speciality,
                           'landing_page': landing_page_, 'specialities': specialities})


def fitness_center(request):
    fitness_centers = FitnessCenterProfile.objects.all().filter(
        user__user__is_active=True)
    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    top_fitness_ = get_top_fitness_center()
    types = FitnessCenterType.objects.all()

    name = request.GET.get('name', '')
    location = request.GET.get('location', '')
    type1 = request.GET.get('type', '')
    if name:
        # fitness_centers = fitness_centers.filter(name__icontains=name)
        fitness_centers = fitness_centers.filter(
            Q(user__username__icontains=name) | Q(name__icontains=name))
    if location:
        # city, country, state = get_city_and_country_from_geo_value(location)
        # fitness_centers = fitness_centers.filter(Q(address__icontains=location) | Q(user__city__icontains=city) |
        #                                         Q(user__country__icontains=country) | Q(user__state__icontains=state))
        fitness_centers = fitness_centers.filter(Q(user__location__icontains=location) | Q(
            address__icontains=location) | Q(address2__icontains=location) | Q(address3__icontains=location))
    if type1:
        # city, country, state = get_city_and_country_from_geo_value(location)
        # fitness_centers = fitness_centers.filter(Q(address__icontains=location) | Q(user__city__icontains=city) |
        #                                         Q(user__country__icontains=country) | Q(user__state__icontains=state))
        fitness_centers = fitness_centers.filter(
            Q(fitness_center_type__name=type1))
    page = request.GET.get('page', 1)
    page = request.GET.get('page', 1)
    paginator = Paginator(fitness_centers, 10)
    try:
        fitness_centers = paginator.page(page)
    except PageNotAnInteger:
        fitness_centers = paginator.page(10)
    except EmptyPage:
        fitness_centers = paginator.page(paginator.num_pages)

    return render(request, 'client/fitness-center.html',
                  context={'fitness_center': fitness_centers, 'top_fitness': top_fitness_,
                           'name': name, 'location': location,
                           'types': types, 'landing_page': landing_page_})


def fitness_models(request):
    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    fitness_models_ = FitnessModalProfile.objects.all()
    top_fitness_ = get_top_fitness_model()
    # modeling_interests = Activities.objects.all()
    modeling_interests = FitnessModalProfile.objects.all()

    name = request.GET.get('name', '')
    interests = request.GET.get('interests', '')
    experience = request.GET.get('experience')
    location = request.GET.get('location', '')

    if name:
        # fitness_models_ = fitness_models_.filter(name__icontains=name)
        fitness_models_ = fitness_models_.filter(
            Q(user__username__icontains=name) | Q(name__icontains=name))
    if location:
        # city, country, state = get_city_and_country_from_geo_value(location)
        # fitness_models_ = fitness_models_.filter(Q(address__icontains=location) | Q(user__city__icontains=city) |
        #                                        Q(user__country__icontains=country) | Q(user__state__icontains=state))
        fitness_models_ = fitness_models_.filter(
            Q(user__location__icontains=location) | Q(address__icontains=location))
    
    if interests:
        fitness_models_ = fitness_models_.filter(
            modeling_interests__contains=interests)

    if request.GET.get('name', '') or request.GET.get('interests', '') or request.GET.get('location', ''):
        pass
    else:
        fitness_models_ = FitnessModalProfile.objects.all()
        activities = Activities.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(fitness_models_, 10)
    try:
        fitness_models_ = paginator.page(page)
    except PageNotAnInteger:
        fitness_models_ = paginator.page(10)
    except EmptyPage:
        fitness_models_ = paginator.page(paginator.num_pages)

    return render(request, 'client/fitness-models.html',
                  context={'fitness_models': fitness_models_, 'top_fitness': top_fitness_,
                           'modeling_interests': modeling_interests,
                           'interests': interests, 'name': name, 'location': location,
                           'landing_page': landing_page_, 'activities':activities})


def blog_details(request):
    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    id_ = request.GET.get('blog_id')
    blog = Blog.objects.get(id=int(id_))
    hearts = Blog_Heart_Modal.objects.filter(blog_id=int(id_)).count()
    return render(request, 'client/blog-details.html', context={'blog': blog, 'landing_page': landing_page_, 'hearts':hearts})


@ login_required
def profile(request):
    global active
    if request.user.is_superuser:
        return redirect('/')

    active_profile = 'info_tab'
    error_message = ''
    is_authenticated_user = True
    storage = get_messages(request)
    for obj in storage:
        active_profile = str(obj).strip()
        if obj.tags == 'error':
            error_message = str(obj).strip()

    storage.used = True
    if not active_profile:
        active_profile = 'info_tab'

    if active_profile in ALLOWED_TABS:
        pass
    else:
        active_profile = 'info_tab'

    profile_ = {}
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        profile_ = get_fitness_professional_profile(user_detail)
    if user_detail.active_user_role.name == FITNESS_MODAL:
        profile_ = get_fitness_modal_profile(user_detail)
    if user_detail.active_user_role.name == FITNESS_CENTER:
        profile_ = get_fitness_center_profile(user_detail)

    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    specialities = Specialities.objects.all()
    activities = Activities.objects.all()
    certifications = Certificationss.objects.all()
    fitness_center_types = FitnessCenterTypes.objects.all()
    fitness_professionals = FitnessProfessionalProfile.objects.all()
    ethnicity = EthnicityTypes.objects.all()
    skin_type = SkinTone.objects.all()
    eye_color = EyeColor.objects.all()
    hair_color = HairColor.objects.all()
    tattoos = Tattoos.objects.all()
    body_types = BodyTypes.objects.all()
    diet_types = DietTypes.objects.all()
    client_preferences = ClientPreferences.objects.all()
    compensation = Compensation.objects.all()
    modeling_interests = ModellingInterests.objects.all()
    roles = UserRoles.objects.all()
    countries = Countries.objects.all()
    time_zones = TimeZone.objects.all()

    if user_detail.active_user_role.name == "Fitness Center":
        active = "center"
    elif user_detail.active_user_role.name == "Fitness Professional":
        active = "pro"
    else:
        active = "model"

    context = {'profile': profile_, 'landing_page': landing_page_, 'activities': activities,
               'specialities': specialities, 'certifications': certifications,
               'fitness_professionals': fitness_professionals,
               'active_profile': active_profile,
               'roles': roles,
               'time_zones': time_zones,
               'countries': countries,
               'ethnicity': ethnicity,
               'compensation': compensation,
               'modeling_interests': modeling_interests,
               'skin_type': skin_type,
               'eye_color': eye_color,
               'hair_color': hair_color,
               'tattoos': tattoos,
               'body_types': body_types,
               'diet_types': diet_types,
               'client_preferences': client_preferences,
               'error_message': error_message,
               'is_authenticated_user': is_authenticated_user,
               'fitness_center_types': fitness_center_types,
               'active': active,
               'map': get_map_object(profile_)}
    return render(request, 'client/ProfileModule/profile_base.html', context=context)


def profile_page(request):
    if request.user.is_authenticated:
        return redirect('client:profile')

    user_id = request.GET.get('profile_id')
    profile_ = {}
    user_detail = UserProfile.objects.get(id=int(user_id))

    if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        profile_ = get_fitness_professional_profile(user_detail)
    if user_detail.active_user_role.name == FITNESS_MODAL:
        profile_ = get_fitness_modal_profile(user_detail)
    if user_detail.active_user_role.name == FITNESS_CENTER:
        profile_ = get_fitness_center_profile(user_detail)

    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)

    context = {'profile': profile_, 'landing_page': landing_page_}
    return render(request, 'client/profile_page.html', context=context)


def center_profile(request, unique):
    global active
    active = "center"
    try:
        unique = int(unique)
    except Exception as e:
        pass

    if type(unique) == int:
        fcp_ = FitnessCenterProfile.objects.filter(id=unique).last()
    else:
        fcp_ = FitnessCenterProfile.objects.filter(
            profile_url__iexact=unique).last()

    if fcp_:
        profile_ = get_fitness_center_profile(fcp_.user)
    else:
        return redirect('client:home')

    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    active_profile = 'info_tab'

    map = get_map_object(profile_)

    context = {'profile': profile_, 'active': active, 'landing_page': landing_page_, 'is_authenticated_user': False,
               'active_profile': active_profile, 'map': map}
    return render(request, 'client/ProfileModule/profile_base.html', context=context)


def pro_profile(request, unique):
    global active
    active = "pro"
    try:
        unique = int(unique)
    except Exception as e:
        pass

    if type(unique) == int:
        fcp_ = FitnessProfessionalProfile.objects.filter(id=unique).last()
    else:
        fcp_ = FitnessProfessionalProfile.objects.filter(
            profile_url__iexact=unique).last()

    if fcp_:
        profile_ = get_fitness_professional_profile(fcp_.user)
        getUserId = profile_['user_id']
    else:
        return redirect('client:home')

    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    active_profile = 'info_tab'

    map = get_map_object(profile_)
    getHeartObject = Heart_Modal.objects.filter(user=getUserId).count()

    context = {'profile': profile_, 'active': active, 'landing_page': landing_page_, 'is_authenticated_user': False,
               'active_profile': active_profile, 'map': map, 'hearts' : getHeartObject}
    return render(request, 'client/ProfileModule/profile_base.html', context=context,)


def modal_profile(request, unique):
    global active
    active = "model"
    try:
        unique = int(unique)
    except Exception as e:
        pass

    if type(unique) == int:
        fcp_ = FitnessModalProfile.objects.filter(id=unique).last()
    else:
        fcp_ = FitnessModalProfile.objects.filter(
            profile_url__iexact=unique).last()

    if fcp_:
        profile_ = get_fitness_modal_profile(fcp_.user)
    else:
        return redirect('client:home')

    landing_page_, created = LandingPageDetails.objects.get_or_create(id=1)
    active_profile = 'info_tab'
    map = get_map_object(profile_)
    context = {'profile': profile_, 'active': active, 'landing_page': landing_page_, 'is_authenticated_user': False,
               'active_profile': active_profile, 'map': map}
    return render(request, 'client/ProfileModule/profile_base.html', context=context)


def data_dump(request):
    # SponsorsInfo.objects.all().delete()
    # AmbassadorsInfo.objects.all().delete()
    # SuccessStories.objects.all().delete()
    # FitnessProfessionalProfileSuccessStories.objects.all().delete()
    # FitnessModalProfileSuccessStories.objects.all().delete()
    # FitnessCenterProfileSuccessStories.objects.all().delete()

    FitnessCenterProfile.objects.update(profile_url='')
    FitnessProfessionalProfile.objects.update(profile_url='')
    FitnessModalProfile.objects.update(profile_url='')

    FitnessCenterMemberShipType.objects.get_or_create(name='Monthly')
    FitnessCenterMemberShipType.objects.get_or_create(name='Yearly')
    FitnessCenterMemberShipType.objects.get_or_create(name='Weekly')

    UserRoles.objects.get_or_create(name=FITNESS_MODAL)
    UserRoles.objects.get_or_create(name=FITNESS_PROFESSIONAL)
    UserRoles.objects.get_or_create(name=FITNESS_CENTER)

    BlogCategories.objects.get_or_create(slug='nutrition', name='Nutrition')
    BlogCategories.objects.get_or_create(slug='recipes', name='Recipies')
    BlogCategories.objects.get_or_create(slug='workout', name='Workouts')
    BlogCategories.objects.get_or_create(slug='reviews', name='Reviews')
    BlogCategories.objects.get_or_create(slug='news', name='News')
    BlogCategories.objects.get_or_create(slug='music', name='Music')

    BlogCategories.objects.filter(slug='news').update(
        name='Podcasts', slug='podcasts')

    specialities = ['Aerobics', 'Athletic Training', 'Back Pain Prevention/Postrehab',
                    'Biomechanics', 'Bodybuilding', 'Cardio Workouts', 'Clinical Exercise Physiologist',
                    'Core Training', 'Corporate Wellness', 'Cross Fit', 'Diet and Nutrition', 'Executive Fitness',
                    'Exercise Physiology', 'Family Fitness', 'Fat Loss', 'Fitness Assessment', 'Fitness Education',
                    'Flexibility', 'Food and Cooking', 'Group Exercise', 'Injury Prevention', 'Kickboxing',
                    'Kids Fitness', 'Kinesiology', 'Lifestyle Coaching', 'Lower Back Pain', 'Massage Therapy',
                    'Medical Fitness for Chronic Conditions', 'Mens Fitness', 'Mind-Body Fitness',
                    'Nutrition', 'Nutrition Coaching', 'Personal Training', 'Physical Therapy', 'Plyometrics',
                    'Postnatal Fitness', 'Postrehab/Injury Recovery', 'Prenatal Fitness', 'Rehabilitation',
                    'Rope Skipping', 'Senior Fitness', 'Skiing',
                    'Speed and Agility Training', 'Sports Conditioning', 'Sports Nutrition', 'Strength Training',
                    'Stress Management', 'Toning and General Fitness', 'Water Fitness', 'Weight Loss',
                    'Weight Management',
                    'Weight Training', 'Wellness Coaching', 'Wellness/Preventive', 'Womens Fitness'
                    ]
    [Specialities.objects.get_or_create(name=obj) for obj in specialities]

    activities = [
        'Aerobics',
        'Baseball',
        'Basketball',
        'Bicycling',
        'Body Leverage/Bodyweight Training',
        'Bodybuilding',
        'Boot Camps',
        'Boxing',
        'Cardio Machines',
        'Choreography',
        'Circuit Training',
        'Core Conditioning',
        'Cross Country',
        'Cross Fit',
        'Cycling',
        'Dancing',
        'Diving',
        'Equestrian',
        'Football',
        'Golfing',
        'Gymnastics',
        'Gyrotonic, Gyrokinesis',
        'Hiking',
        'Hockey',
        'Ice Skating',
        'Jogging',
        'Kettlebells',
        'Kickboxing',
        'Lacrosse',
        'Martial Arts',
        'Meditation',
        'Mind & Body',
        'Mixed Martial Arts (MMA)',
        'Nia',
        'Nordic Walking',
        'Personal Training',
        'Pilates',
        'Pole Dancing',
        'Pole Fitness',
        'Roller Blading',
        'Rope Skipping',
        'Rowing',
        'Running',
        'Skiing',
        'Snowboarding',
        'Soccer',
        'Softball',
        'Stretching/Flexibility',
        'Surfing',
        'Swimming',
        'Tai Chi',
        'Tennis',
        'Track and Field',
        'Trail Running',
        'Triathlon',
        'TRX (Suspension Training)',
        'Volleyball',
        'Walking',
        'Water Fitness',
        'Water Polo',
        'Wrestling',
        'Yoga',
        'Zumba (Latin Dance)']

    [Activities.objects.get_or_create(name=obj) for obj in activities]

    certifications = [
        'American Aerobic Association International (AAAI)',
        'International Sports Medicine Association (ISMA)',
        'American Academy of Health & Fitness (AAHF)',
        'American Academy of Personal Training (AAPT)',
        'Academy of Applied Personal Training Education (AAPTE)',
        'American Council on Exercise (ACE)',
        'American College of Sports Medicine (ACSM)',
        'Aquatic Exercise Association (AEA)',
        'Alberta Fitness Leadership Certification Association (AFLCA)',
        'American Fitness Professionals Association (AFPA)',
        'American Sports and Fitness Association (ASFA)',
        'Agility Training Institute (ATI)',
        'Balanced Body',
        'Balletone (BT)',
        'BASI Pilates (Basi)',
        'Batuka',
        'BioMechanics',
        'BodyBlade®',
        'Boxing Fitness Institute (BFI)',
        'Body Training Systems (BTS)',
        'Burn with Kearns',
        'BWI National Health Promotion Training Institute (BWI)',
        'canfitpro',
        'C.H.E.K Institute (CHEK)',
        'Chi Running & Walking',
        'Core Fitness Roller',
        'Combine360 (C360)',
        'Cycling Fusion',
        'Dragon Door',
        'Drums Alive (DA)',
        'FallProof',
        'Functional Diagnostic Nutrition (FDN)',
        'Functional Movement Systems (FMS)',
        'FiTour',
        'Fit Pro Academy (FPTA)',
        'Family Safety and Self-Defense Institute (FSI)',
        'Gray Institute',
        'GYROKINESIS®',
        'GYROTONIC®',
        'Healthy-Steps',
        'HOT HULA fitness®',
        'Heart Zones (HZ)',
        'International Fitness Professionals Association (IFPA)',
        'Interactive Fitness Trainers of America (IFTA)',
        'International Sports Sciences Association (ISSA)',
        'International Sports & Fitness Trainers Association (ISFTA)',
        'Kathy Corey Pilates',
        'Keiser Corporation (Keiser)',
        'Ken Baum Mental Edge (KBME)',
        'Kickboxing Fitness Institute (KFI)',
        'KRANKcycle',
        'LeMond RevMaster Indoor Cycle (LeMond)',
        'Les Mills',
        'Life Fitness',
        'Muscle Activation Techniques (MAT)',
        'National Academy of Sports Medicine (NASM)',
        'National Council for Certified Personal Trainers (NCCPT)',
        'National Council on Strength and Fitness (NCSF)',
        'National Exercise & Sports Trainers Association (NESTA)',
        'National Exercise Trainers Association (NETA)',
        'National Federation of Professional Trainers (NFPT)',
        'Nia',
        'National Personal Training Institute (NPTI)',
        'National Posture Institute (NPI)',
        'National Strength and Conditioning Association (NSCA)',
        'National Strength Professionals Association (NSPA)',
        'P90X',
        'Peak Pilates',
        'PHI: Performance Enhancement International',
        'Physicalmind Institute',
        'Pilates Method Alliance (PMA)',
        'Polestar',
        'Powder Blue Productions (PB11)',
        'Power Pilates',
        'PROPTA',
        'PTA Global (PTA)',
        'Punk Rope',
        'Resist-A-Ball®',
        'Revelation Wellness Instructor Training (Revelation Wellness)',
        'R.I.P.P.E.D. - The One Stop Body Shock',
        'Rolf Gates',
        'Schwinn Indoor Cycling (Schwinn)',
        'Shapely Girl Fitness (SGF)',
        'SilverSneakers',
        'Spencer Institute',
        'Spinning®',
        'STOTT PILATES®',
        'Stroller Strides®',
        'TEAM Pilates',
        'The Cooper Institute (CI)',
        'The Pilates Coach',
        'Tina Vindums Outdoor Fitness (Outdoor Fitness)',
        'Training and Wellness Certification Commission (TWCC)',
        'Trigger Point',
        'TRX'
        'Twist Conditioning',
        'U.S. Career Institute (USCI)',
        'VIVOBAREFOOT Training Clinic (VIVOBAREFOOT)',
        'Wellcoaches',
        'World Instructor Training Schools (W.I.T.S.)',
        'YogaWorks'

    ]
    [Certificationss.objects.get_or_create(name=obj) for obj in certifications]

    time_zone = [
        "Africa/Abidjan",
        "Africa/Accra",
        "Africa/Addis_Ababa",
        "Africa/Algiers",
        "Africa/Asmara",
        "Africa/Asmera",
        "Africa/Bamako",
        "Africa/Bangui",
        "Africa/Banjul",
        "Africa/Bissau",
        "Africa/Blantyre",
        "Africa/Brazzaville",
        "Africa/Bujumbura",
        "Africa/Cairo",
        "Africa/Casablanca",
        "Africa/Ceuta",
        "Africa/Conakry",
        "Africa/Dakar",
        "Africa/Dar_es_Salaam",
        "Africa/Djibouti",
        "Africa/Douala",
        "Africa/El_Aaiun",
        "Africa/Freetown",
        "Africa/Gaborone",
        "Africa/Harare",
        "Africa/Johannesburg",
        "Africa/Juba",
        "Africa/Kampala",
        "Africa/Khartoum",
        "Africa/Kigali",
        "Africa/Kinshasa",
        "Africa/Lagos",
        "Africa/Libreville",
        "Africa/Lome",
        "Africa/Luanda",
        "Africa/Lubumbashi",
        "Africa/Lusaka",
        "Africa/Malabo",
        "Africa/Maputo",
        "Africa/Maseru",
        "Africa/Mbabane",
        "Africa/Mogadishu",
        "Africa/Monrovia",
        "Africa/Nairobi",
        "Africa/Ndjamena",
        "Africa/Niamey",
        "Africa/Nouakchott",
        "Africa/Ouagadougou",
        "Africa/Porto-Novo",
        "Africa/Sao_Tome",
        "Africa/Timbuktu",
        "Africa/Tripoli",
        "Africa/Tunis",
        "Africa/Windhoek",
        "AKST9AKDT",
        "America/Adak",
        "America/Anchorage",
        "America/Anguilla",
        "America/Antigua",
        "America/Araguaina",
        "America/Argentina/Buenos_Aires",
        "America/Argentina/Catamarca",
        "America/Argentina/ComodRivadavia",
        "America/Argentina/Cordoba",
        "America/Argentina/Jujuy",
        "America/Argentina/La_Rioja",
        "America/Argentina/Mendoza",
        "America/Argentina/Rio_Gallegos",
        "America/Argentina/Salta",
        "America/Argentina/San_Juan",
        "America/Argentina/San_Luis",
        "America/Argentina/Tucuman",
        "America/Argentina/Ushuaia",
        "America/Aruba",
        "America/Asuncion",
        "America/Atikokan",
        "America/Atka",
        "America/Bahia",
        "America/Bahia_Banderas",
        "America/Barbados",
        "America/Belem",
        "America/Belize",
        "America/Blanc-Sablon",
        "America/Boa_Vista",
        "America/Bogota",
        "America/Boise",
        "America/Buenos_Aires",
        "America/Cambridge_Bay",
        "America/Campo_Grande",
        "America/Cancun",
        "America/Caracas",
        "America/Catamarca",
        "America/Cayenne",
        "America/Cayman",
        "America/Chicago",
        "America/Chihuahua",
        "America/Coral_Harbour",
        "America/Cordoba",
        "America/Costa_Rica",
        "America/Creston",
        "America/Cuiaba",
        "America/Curacao",
        "America/Danmarkshavn",
        "America/Dawson",
        "America/Dawson_Creek",
        "America/Denver",
        "America/Detroit",
        "America/Dominica",
        "America/Edmonton",
        "America/Eirunepe",
        "America/El_Salvador",
        "America/Ensenada",
        "America/Fort_Wayne",
        "America/Fortaleza",
        "America/Glace_Bay",
        "America/Godthab",
        "America/Goose_Bay",
        "America/Grand_Turk",
        "America/Grenada",
        "America/Guadeloupe",
        "America/Guatemala",
        "America/Guayaquil",
        "America/Guyana",
        "America/Halifax",
        "America/Havana",
        "America/Hermosillo",
        "America/Indiana/Indianapolis",
        "America/Indiana/Knox",
        "America/Indiana/Marengo",
        "America/Indiana/Petersburg",
        "America/Indiana/Tell_City",
        "America/Indiana/Vevay",
        "America/Indiana/Vincennes",
        "America/Indiana/Winamac",
        "America/Indianapolis",
        "America/Inuvik",
        "America/Iqaluit",
        "America/Jamaica",
        "America/Jujuy",
        "America/Juneau",
        "America/Kentucky/Louisville",
        "America/Kentucky/Monticello",
        "America/Knox_IN",
        "America/Kralendijk",
        "America/La_Paz",
        "America/Lima",
        "America/Los_Angeles",
        "America/Louisville",
        "America/Lower_Princes",
        "America/Maceio",
        "America/Managua",
        "America/Manaus",
        "America/Marigot",
        "America/Martinique",
        "America/Matamoros",
        "America/Mazatlan",
        "America/Mendoza",
        "America/Menominee",
        "America/Merida",
        "America/Metlakatla",
        "America/Mexico_City",
        "America/Miquelon",
        "America/Moncton",
        "America/Monterrey",
        "America/Montevideo",
        "America/Montreal",
        "America/Montserrat",
        "America/Nassau",
        "America/New_York",
        "America/Nipigon",
        "America/Nome",
        "America/Noronha",
        "America/North_Dakota/Beulah",
        "America/North_Dakota/Center",
        "America/North_Dakota/New_Salem",
        "America/Ojinaga",
        "America/Panama",
        "America/Pangnirtung",
        "America/Paramaribo",
        "America/Phoenix",
        "America/Port_of_Spain",
        "America/Port-au-Prince",
        "America/Porto_Acre",
        "America/Porto_Velho",
        "America/Puerto_Rico",
        "America/Rainy_River",
        "America/Rankin_Inlet",
        "America/Recife",
        "America/Regina",
        "America/Resolute",
        "America/Rio_Branco",
        "America/Rosario",
        "America/Santa_Isabel",
        "America/Santarem",
        "America/Santiago",
        "America/Santo_Domingo",
        "America/Sao_Paulo",
        "America/Scoresbysund",
        "America/Shiprock",
        "America/Sitka",
        "America/St_Barthelemy",
        "America/St_Johns",
        "America/St_Kitts",
        "America/St_Lucia",
        "America/St_Thomas",
        "America/St_Vincent",
        "America/Swift_Current",
        "America/Tegucigalpa",
        "America/Thule",
        "America/Thunder_Bay",
        "America/Tijuana",
        "America/Toronto",
        "America/Tortola",
        "America/Vancouver",
        "America/Virgin",
        "America/Whitehorse",
        "America/Winnipeg",
        "America/Yakutat",
        "America/Yellowknife",
        "Antarctica/Casey",
        "Antarctica/Davis",
        "Antarctica/DumontDUrville",
        "Antarctica/Macquarie",
        "Antarctica/Mawson",
        "Antarctica/McMurdo",
        "Antarctica/Palmer",
        "Antarctica/Rothera",
        "Antarctica/South_Pole",
        "Antarctica/Syowa",
        "Antarctica/Vostok",
        "Arctic/Longyearbyen",
        "Asia/Aden",
        "Asia/Almaty",
        "Asia/Amman",
        "Asia/Anadyr",
        "Asia/Aqtau",
        "Asia/Aqtobe",
        "Asia/Ashgabat",
        "Asia/Ashkhabad",
        "Asia/Baghdad",
        "Asia/Bahrain",
        "Asia/Baku",
        "Asia/Bangkok",
        "Asia/Beirut",
        "Asia/Bishkek",
        "Asia/Brunei",
        "Asia/Calcutta",
        "Asia/Choibalsan",
        "Asia/Chongqing",
        "Asia/Chungking",
        "Asia/Colombo",
        "Asia/Dacca",
        "Asia/Damascus",
        "Asia/Dhaka",
        "Asia/Dili",
        "Asia/Dubai",
        "Asia/Dushanbe",
        "Asia/Gaza",
        "Asia/Harbin",
        "Asia/Hebron",
        "Asia/Ho_Chi_Minh",
        "Asia/Hong_Kong",
        "Asia/Hovd",
        "Asia/Irkutsk",
        "Asia/Istanbul",
        "Asia/Jakarta",
        "Asia/Jayapura",
        "Asia/Jerusalem",
        "Asia/Kabul",
        "Asia/Kamchatka",
        "Asia/Karachi",
        "Asia/Kashgar",
        "Asia/Kathmandu",
        "Asia/Katmandu",
        "Asia/Kolkata",
        "Asia/Krasnoyarsk",
        "Asia/Kuala_Lumpur",
        "Asia/Kuching",
        "Asia/Kuwait",
        "Asia/Macao",
        "Asia/Macau",
        "Asia/Magadan",
        "Asia/Makassar",
        "Asia/Manila",
        "Asia/Muscat",
        "Asia/Nicosia",
        "Asia/Novokuznetsk",
        "Asia/Novosibirsk",
        "Asia/Omsk",
        "Asia/Oral",
        "Asia/Phnom_Penh",
        "Asia/Pontianak",
        "Asia/Pyongyang",
        "Asia/Qatar",
        "Asia/Qyzylorda",
        "Asia/Rangoon",
        "Asia/Riyadh",
        "Asia/Saigon",
        "Asia/Sakhalin",
        "Asia/Samarkand",
        "Asia/Seoul",
        "Asia/Shanghai",
        "Asia/Singapore",
        "Asia/Taipei",
        "Asia/Tashkent",
        "Asia/Tbilisi",
        "Asia/Tehran",
        "Asia/Tel_Aviv",
        "Asia/Thimbu",
        "Asia/Thimphu",
        "Asia/Tokyo",
        "Asia/Ujung_Pandang",
        "Asia/Ulaanbaatar",
        "Asia/Ulan_Bator",
        "Asia/Urumqi",
        "Asia/Vientiane",
        "Asia/Vladivostok",
        "Asia/Yakutsk",
        "Asia/Yekaterinburg",
        "Asia/Yerevan",
        "Atlantic/Azores",
        "Atlantic/Bermuda",
        "Atlantic/Canary",
        "Atlantic/Cape_Verde",
        "Atlantic/Faeroe",
        "Atlantic/Faroe",
        "Atlantic/Jan_Mayen",
        "Atlantic/Madeira",
        "Atlantic/Reykjavik",
        "Atlantic/South_Georgia",
        "Atlantic/St_Helena",
        "Atlantic/Stanley",
        "Australia/ACT",
        "Australia/Adelaide",
        "Australia/Brisbane",
        "Australia/Broken_Hill",
        "Australia/Canberra",
        "Australia/Currie",
        "Australia/Darwin",
        "Australia/Eucla",
        "Australia/Hobart",
        "Australia/LHI",
        "Australia/Lindeman",
        "Australia/Lord_Howe",
        "Australia/Melbourne",
        "Australia/North",
        "Australia/NSW",
        "Australia/Perth",
        "Australia/Queensland",
        "Australia/South",
        "Australia/Sydney",
        "Australia/Tasmania",
        "Australia/Victoria",
        "Australia/West",
        "Australia/Yancowinna",
        "Brazil/Acre",
        "Brazil/DeNoronha",
        "Brazil/East",
        "Brazil/West",
        "Canada/Atlantic",
        "Canada/Central",
        "Canada/Eastern",
        "Canada/East-Saskatchewan",
        "Canada/Mountain",
        "Canada/Newfoundland",
        "Canada/Pacific",
        "Canada/Saskatchewan",
        "Canada/Yukon",
        "CET",
        "Chile/Continental",
        "Chile/EasterIsland",
        "CST6CDT",
        "Cuba",
        "EET",
        "Egypt",
        "Eire",
        "EST",
        "EST5EDT",
        "Etc./GMT",
        "Etc./GMT+0",
        "Etc./UCT",
        "Etc./Universal",
        "Etc./UTC",
        "Etc./Zulu",
        "Europe/Amsterdam",
        "Europe/Andorra",
        "Europe/Athens",
        "Europe/Belfast",
        "Europe/Belgrade",
        "Europe/Berlin",
        "Europe/Bratislava",
        "Europe/Brussels",
        "Europe/Bucharest",
        "Europe/Budapest",
        "Europe/Chisinau",
        "Europe/Copenhagen",
        "Europe/Dublin",
        "Europe/Gibraltar",
        "Europe/Guernsey",
        "Europe/Helsinki",
        "Europe/Isle_of_Man",
        "Europe/Istanbul",
        "Europe/Jersey",
        "Europe/Kaliningrad",
        "Europe/Kiev",
        "Europe/Lisbon",
        "Europe/Ljubljana",
        "Europe/London",
        "Europe/Luxembourg",
        "Europe/Madrid",
        "Europe/Malta",
        "Europe/Mariehamn",
        "Europe/Minsk",
        "Europe/Monaco",
        "Europe/Moscow",
        "Europe/Nicosia",
        "Europe/Oslo",
        "Europe/Paris",
        "Europe/Podgorica",
        "Europe/Prague",
        "Europe/Riga",
        "Europe/Rome",
        "Europe/Samara",
        "Europe/San_Marino",
        "Europe/Sarajevo",
        "Europe/Simferopol",
        "Europe/Skopje",
        "Europe/Sofia",
        "Europe/Stockholm",
        "Europe/Tallinn",
        "Europe/Tirane",
        "Europe/Tiraspol",
        "Europe/Uzhgorod",
        "Europe/Vaduz",
        "Europe/Vatican",
        "Europe/Vienna",
        "Europe/Vilnius",
        "Europe/Volgograd",
        "Europe/Warsaw",
        "Europe/Zagreb",
        "Europe/Zaporozhye",
        "Europe/Zurich",
        "GB",
        "GB-Eire",
        "GMT",
        "GMT+0",
        "GMT0",
        "GMT-0",
        "Greenwich",
        "Hong Kong",
        "HST",
        "Iceland",
        "Indian/Antananarivo",
        "Indian/Chagos",
        "Indian/Christmas",
        "Indian/Cocos",
        "Indian/Comoro",
        "Indian/Kerguelen",
        "Indian/Mahe",
        "Indian/Maldives",
        "Indian/Mauritius",
        "Indian/Mayotte",
        "Indian/Reunion",
        "Iran",
        "Israel",
        "Jamaica",
        "Japan",
        "JST-9",
        "Kwajalein",
        "Libya",
        "MET",
        "Mexico/BajaNorte",
        "Mexico/BajaSur",
        "Mexico/General",
        "MST",
        "MST7MDT",
        "Navajo",
        "NZ",
        "NZ-CHAT",
        "Pacific/Apia",
        "Pacific/Auckland",
        "Pacific/Chatham",
        "Pacific/Chuuk",
        "Pacific/Easter",
        "Pacific/Efate",
        "Pacific/Enderbury",
        "Pacific/Fakaofo",
        "Pacific/Fiji",
        "Pacific/Funafuti",
        "Pacific/Galapagos",
        "Pacific/Gambier",
        "Pacific/Guadalcanal",
        "Pacific/Guam",
        "Pacific/Honolulu",
        "Pacific/Johnston",
        "Pacific/Kiritimati",
        "Pacific/Kosrae",
        "Pacific/Kwajalein",
        "Pacific/Majuro",
        "Pacific/Marquesas",
        "Pacific/Midway",
        "Pacific/Nauru",
        "Pacific/Niue",
        "Pacific/Norfolk",
        "Pacific/Noumea",
        "Pacific/Pago_Pago",
        "Pacific/Palau",
        "Pacific/Pitcairn",
        "Pacific/Pohnpei",
        "Pacific/Ponape",
        "Pacific/Port_Moresby",
        "Pacific/Rarotonga",
        "Pacific/Saipan",
        "Pacific/Samoa",
        "Pacific/Tahiti",
        "Pacific/Tarawa",
        "Pacific/Tongatapu",
        "Pacific/Truk",
        "Pacific/Wake",
        "Pacific/Wallis",
        "Pacific/Yap",
        "Poland",
        "Portugal",
        "PRC",
        "PST8PDT",
        "ROC",
        "ROK",
        "Singapore",
        "Turkey",
        "UCT",
        "Universal",
        "US/Alaska",
        "US/Aleutian",
        "US/Arizona",
        "US/Central",
        "US/Eastern",
        "US/East-Indiana",
        "US/Hawaii",
        "US/Indiana-Starke",
        "US/Michigan",
        "US/Mountain",
        "US/Pacific",
        "US/Pacific-New",
        "US/Samoa",
        "UTC",
        "WET",
        "W-SU",
        "Zulu"]
    [TimeZone.objects.get_or_create(name=obj) for obj in time_zone]

    fitness_center_types = [

        'Aerobic Center',
        'Athletic Club',
        'Boxing Club',
        'Calisthenics Center',
        'Cycling Club',
        'Country Club',
        'Cross Fit',
        'Cross Training',
        'Dance Center',
        'Equestrian Center',
        'Gym',
        'Gymnastics',
        'Kick Boxing',
        'Martial Arts',
        'Olympic Style Gym',
        'Personal Training Club',
        'Pilates Center',
        'Pole Dancing Studio',
        'Recreation Center',
        'Running Center',
        'Skiing Club',
        'Skipping Club',
        'Spinning Center',
        'Studio',
        'Swimming Center',
        'Training Studio',
        'Yoga Center',
        'Zumba Studio'

    ]

    countries = [
        "Afghanistan",
        "Albania",
        "Algeria",
        "Andorra",
        "Angola",
        "Antigua_and_Barbuda",
        "Argentina",
        "Armenia",
        "Australia",
        "Austria",
        "Azerbaijan",
        "Bahamas",
        "Bahrain",
        "Bangladesh",
        "Barbados",
        "Belarus",
        "Belgium",
        "Belize",
        "Benin",
        "Bhutan",
        "Bolivia",
        "Bosnia_and_Herzegovina",
        "Botswana",
        "Brazil",
        "Brunei",
        "Bulgaria",
        "Burkina_Faso",
        "Burundi",
        "Cambodia",
        "Cameroon",
        "Canada",
        "Cape_Verde",
        "Central_African_Republic",
        "Chad",
        "Chile",
        "China",
        "Colombia",
        "Comoros",
        "Cook_Islands"
        "Costa_Rica",
        "Croatia",
        "Cuba",
        "Cyprus",
        "Czech_Republic",
        "Denmark",
        "Djibouti",
        "Dominica",
        "Dominican_Republic",
        "East_Timor",
        "Ecuador",
        "Egypt",
        "El_Salvador",
        "Equatorial_Guinea",
        "Eritrea",
        "Estonia",
        "Ethiopia",
        "Fiji",
        "Finland",
        "France",
        "Gabon",
        "The_Gambia",
        "Georgia",
        "Germany",
        "Ghana",
        "Greece",
        "Grenada",
        "Guatemala",
        "Guinea",
        "Guinea-Bissau",
        "Guyana",
        "Haiti",
        "Honduras",
        "Hungary",
        "Iceland",
        "India",
        "Indonesia",
        "Iran",
        "Iraq",
        "Ireland",
        "Israel",
        "Italy",
        "Jamaica",
        "Japan",
        "Jordan",
        "Kazakhstan",
        "Kenya",
        "Kiribati",
        "Kuwait",
        "Kyrgyzstan",
        "Laos",
        "Latvia",
        "Lebanon",
        "Lesotho",
        "Liberia",
        "Libya",
        "Liechtenstein",
        "Lithuania",
        "Luxembourg",
        "Macedonia",
        "Madagascar",
        "Malawi",
        "Malaysia",
        "Maldives",
        "Mali",
        "Malta",
        "Marshall_Islands",
        "Mauritania",
        "Mauritius",
        "Mexico",
        "Moldova",
        "Monaco",
        "Mongolia",
        "Montenegro",
        "Morocco",
        "Mozambique",
        "Myanmar",
        "Namibia",
        "Nauru",
        "Nepal",
        "Netherlands",
        "New_Zealand",
        "Nicaragua",
        "Niger",
        "Nigeria",
        "Norway",
        "Oman",
        "Pakistan",
        "Palau",
        "Panama",
        "Papua_New_Guinea",
        "Paraguay",
        "Peru",
        "Philippines",
        "Poland",
        "Portugal",
        "Qatar",
        "Romania",
        "Russia",
        "Rwanda",
        "Saint_Kitts_and_Nevis",
        "Saint_Lucia",
        "Saint_Vincent_and_the_Grenadines",
        "Samoa",
        "San_Marino",
        "Sao_Tome_and_Principe",
        "Saudi_Arabia",
        "Senegal",
        "Serbia",
        "Seychelles",
        "Sierra_Leone",
        "Singapore",
        "Slovakia",
        "Slovenia",
        "Solomon_Islands",
        "Somalia",
        "South_Africa",
        "South_Sudan",
        "Spain",
        "Sri_Lanka",
        "Sudan",
        "Suriname",
        "Swaziland",
        "Sweden",
        "Switzerland",
        "Syria",
        "Taiwan",
        "Tajikistan",
        "Tanzania",
        "Thailand",
        "Togo",
        "Tonga",
        "Trinidad_and_Tobago",
        "Tunisia",
        "Turkey",
        "Turkmenistan",
        "Tuvalu",
        "Uganda",
        "Ukraine",
        "United_Arab_Emirates",
        "United_Kingdom",
        "United_States",
        "Uruguay",
        "Uzbekistan",
        "Vanuatu",
        "Venezuela",
        "Vietnam",
        "Yemen",
        "Zambia",
        "Zimbabwe"
    ]

    [Countries.objects.get_or_create(name=obj) for obj in countries]

    [FitnessCenterType.objects.get_or_create(
        name=obj) for obj in fitness_center_types]

    ethnicity = ['Asian', 'Caucasian', 'Eastern European', 'East Indian', 'Hispanic',
                 'Middle Eastern', 'Native American', 'Pacific Islander', 'I don’t know']

    [EthnicityTypes.objects.get_or_create(name=obj) for obj in ethnicity]

    skin_tone = ['Light', 'Fair', 'Medium', 'Olive',
                 'Tan', 'Brown', 'Dark Brown', 'Black']
    [SkinTone.objects.get_or_create(name=obj) for obj in skin_tone]

    eye_color = ['Amber', 'Blue', 'Brown', 'Dark Brown',
                 'Grey', 'Green', 'Hazel', 'Red', 'Violet']
    [EyeColor.objects.get_or_create(name=obj) for obj in eye_color]

    hair_color = ['Bald', 'Long', 'Medium ',
                  'Short', 'Shoulder Length', 'Very Long']
    [HairColor.objects.get_or_create(name=obj) for obj in hair_color]

    tatoos = ['None', 'Some', 'Many']
    [Tattoos.objects.get_or_create(name=obj) for obj in tatoos]

    body_type = ['Ectomorph', 'Endomorph', 'Mesomorph']
    [BodyTypes.objects.get_or_create(name=obj) for obj in body_type]

    diet_type = ['Regular', 'Vegan', 'Raw Food', 'Mediterranean']
    [DietTypes.objects.get_or_create(name=obj) for obj in diet_type]

    client_pref = ['Untrained', 'Novice', 'Intermediate',
                   'Advanced', 'Elite', 'All Levels']
    [ClientPreferences.objects.get_or_create(name=obj) for obj in client_pref]

    modeling_interests = ['Acting', 'Art', 'Body paint', 'Cosplay', 'Dance', 'Editorial',
                          'Fashion', 'Fit Modeling', 'Fitness', 'Hair/Makeup', 'Lifestyle',
                          'Lingerie', 'Parts Modeling', 'Performance Artist', 'Pinup',
                          'Pregnancy', 'Promotional Modeling', 'Runaway', 'Spokesperson / Host',
                          'Sport ', 'Stunt', 'Swimwear', 'Underwater']
    [ModellingInterests.objects.get_or_create(
        name=obj) for obj in modeling_interests]

    compensations_ = ['Paid Assignments', 'Any',
                      'Depends on assignment', 'Time for Print']
    [Compensation.objects.get_or_create(name=obj) for obj in compensations_]
    return redirect('/')


@ login_required
def about_info_update(request):
    user_detail = UserProfile.objects.get(user=request.user)

    try:
        countVideo = request.POST['total_video_links']
        countVideo = int(countVideo)
    except:
        return redirect('/accounts/details')

    if user_detail.active_user_role.name == FITNESS_CENTER:
        fcp = FitnessCenterProfile.objects.get(user=user_detail)
        for i in range(countVideo):
            try:
                video_link_ = request.POST[('video_link'+str(i))]
                try:
                    category_ = request.POST[('category'+str(i))]
                except:
                    category_ = 'OTHER'
                FitnessCenterYoutubeVideoLinks.objects.create(user=fcp, video_link =video_link_, category=category_)
            except:
                pass
    elif user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        fcp = FitnessProfessionalProfile.objects.get(user=user_detail)
        for i in range(countVideo):
            try:
                video_link_ = request.POST[('video_link'+str(i))]
                try:
                    category_ = request.POST[('category'+str(i))]
                except:
                    category_ = 'OTHER'
                FitnessProfessionalYoutubeVideoLinks.objects.create(user=fcp, video_link =video_link_, category = category_)
            except:
                pass
    else:
        fcp = FitnessModalProfile.objects.get(user=user_detail)
        for i in range(countVideo):
            try:
                video_link_ = request.POST[('video_link'+str(i))]
                try:
                    category_ = request.POST[('category'+str(i))]
                except:
                    category_ = 'OTHER'
                FitnessModelYoutubeVideoLinks.objects.create(user=fcp, video_link =video_link_, category =category_)
            except:
                pass

    
    


    # about_us = request.POST['about_us']
    # video_code = request.POST['video_code']
    # video_code2 = request.POST['video_code2']
    # video_code3 = request.POST['video_code3']
    # video_code4 = request.POST['video_code4']
    # if "youtube" not in video_code:
    #     if "vimeo" not in video_code:
    #         video_code = video_code.replace(
    #             "https://www.dailymotion.com/", "https://www.dailymotion.com/embed/")
    #     else:
    #         video_code = video_code.replace(
    #             "https://vimeo.com/", "https://player.vimeo.com/video/")
    #     print("vimeo1")
    # else:
    #     video_code = video_code.replace("watch?v=", "embed/")
    #     video_code = video_code.split('&')[0]
    #     print("youtube1")
    # if "youtube" not in video_code2:
    #     if "vimeo" not in video_code2:
    #         video_code2 = video_code2.replace(
    #             "https://www.dailymotion.com/", "https://www.dailymotion.com/embed/")
    #     else:
    #         video_code2 = video_code2.replace(
    #             "https://vimeo.com/", "https://player.vimeo.com/video/")
    #     print("vimeo2")
    # else:
    #     video_code2 = video_code2.replace("watch?v=", "embed/")
    #     video_code2 = video_code2.split('&')[0]
    #     print("youtube2")
    # if "youtube" not in video_code3:
    #     if "vimeo" not in video_code3:
    #         video_code3 = video_code3.replace(
    #             "https://www.dailymotion.com/", "https://www.dailymotion.com/embed/")
    #     else:
    #         video_code3 = video_code3.replace(
    #             "https://vimeo.com/", "https://player.vimeo.com/video/")
    #     print("vimeo3")
    # else:
    #     video_code3 = video_code3.replace("watch?v=", "embed/")
    #     video_code3 = video_code3.split('&')[0]
    #     print("youtube3")
    # if "youtube" not in video_code4:
    #     if "vimeo" not in video_code4:
    #         video_code4 = video_code4.replace(
    #             "https://www.dailymotion.com/", "https://www.dailymotion.com/embed/")
    #     else:
    #         video_code4 = video_code4.replace(
    #             "https://vimeo.com/", "https://player.vimeo.com/video/")
    #     print("vimeo4")
    # else:
    #     video_code4 = video_code4.replace("watch?v=", "embed/")
    #     video_code4 = video_code4.split('&')[0]
    #     print("youtube4")

    fcp.about_us = about_us
    # fcp.video_code = video_code
    # fcp.video_code2 = video_code2
    # fcp.video_code3 = video_code3
    # fcp.video_code4 = video_code4
    fcp.save()

    messages.info(request, 'about_tab')
    return redirect('client:profile')


@ login_required
def update_profile_image(request):
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        fcp = FitnessCenterProfile.objects.get(user=user_detail)
    elif user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        fcp = FitnessProfessionalProfile.objects.get(user=user_detail)
    else:
        fcp = FitnessModalProfile.objects.get(user=user_detail)

    import base64
    from django.core.files.base import ContentFile

    profile_image = request.POST['profile_image_base64']

    format, imgstr = profile_image.split(';base64,')
    ext = format.split('/')[-1]
    profile_image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

    # profile_image = request.FILES['profile_image']

    fcp.profile_image = profile_image
    fcp.save()
    return redirect('client:profile')


@ login_required
def update_user_role(request):
    user_detail = UserProfile.objects.get(user=request.user)

    role_switch = request.POST['role_switch']
    role_switch = UserRoles.objects.get(id=int(role_switch))
    user_detail.active_user_role = role_switch
    user_detail.roles.add(role_switch)
    user_detail.save()

    if role_switch.name == FITNESS_MODAL:
        FitnessModalProfile.objects.get_or_create(user=user_detail)
    if role_switch.name == FITNESS_PROFESSIONAL:
        FitnessProfessionalProfile.objects.get_or_create(user=user_detail)
    if role_switch.name == FITNESS_CENTER:
        FitnessCenterProfile.objects.get_or_create(user=user_detail)

    return redirect('client:profile')


@ login_required
def update_location_info(request):
    user_detail = UserProfile.objects.get(user=request.user)

    location = request.POST['location']
    # timezone = request.POST['timezone']
    city, country, state = get_city_and_country_from_geo_value(location)

    user_detail.city = city
    user_detail.country = country
    user_detail.state = state
    user_detail.location = location
    # user_detail.timezone = timezone
    user_detail.save()

    return redirect('client:profile')


@ login_required
def update_info_tab(request):
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        specialities = request.POST.getlist('specialities')
        languages = request.POST.getlist('languages')
        hours_of_operation = request.POST['hours_of_operation']
        awards = request.POST['awards']
        # brands = request.POST['brands']
        about_us = request.POST['about_us']
        member_ship_plans = request.POST['member_ship_plans']
        profile_image = request.FILES['profile_image'] if 'profile_image' in request.FILES else None
        fitness_pros = request.POST.getlist(
            'fitness_pros') if 'fitness_pros' in request.POST else None
        specialities = ", ".join(specialities)
        languages = ", ".join(languages)
        open_since = request.POST['open_since']
        fitness_center = request.POST['fitness_center']
        prod_name_review_value = request.POST['productNameReviewValue']
        prod_review_value = request.POST['productReviewValue']
        prod_review_star_value = request.POST['productReviewStarValue']

        prod_name_review_value = prod_name_review_value.split("','")
        prod_name_review_value = [x.replace("'", '') for x in prod_name_review_value]
        prod_review_value = prod_review_value.split("','")
        prod_review_value = [x.replace("'", '') for x in prod_review_value]
        prod_review_star_value = prod_review_star_value.split("','")
        prod_review_star_value = [x.replace("'", '') for x in prod_review_star_value]

        list_ = []
        try:
            for obj in range(len(prod_name_review_value)):
                list_.append({'name': prod_name_review_value[obj], 'review': prod_review_value[obj],
                              'star': int(prod_review_star_value[obj])})
        except:
            list_ = []

        list_ = json.dumps(list_)
        fcp = FitnessCenterProfile.objects.get(user=user_detail)
        fcp.specialities = specialities
        fcp.languages = languages
        fcp.hours_of_operation = hours_of_operation
        fcp.about_us = about_us
        # fcp.brands = brands
        fcp.awards = awards
        fcp.member_ship_plans = member_ship_plans
        fcp.open_since = open_since
        fcp.product_reviews = list_
        fcp.fitness_center_type = FitnessCenterType.objects.get(id=int(fitness_center))

        if fitness_pros:
            fcp.fitness_pros.remove(*fcp.fitness_pros.all())

            for obj in fitness_pros:
                fcp.fitness_pros.add(
                    FitnessProfessionalProfile.objects.get(id=int(obj)))
        else:
            fcp.fitness_pros.remove(*fcp.fitness_pros.all())

        if profile_image:
            fcp.profile_image = profile_image

        fcp.save()

    if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        business_name = request.POST['business_name']
        degree = request.POST['degree']
        # brands = request.POST['brands']
        professions = request.POST['professions']
        training_rates = request.POST['training_rates']
        client_preferences = request.POST['client_preferences']
        certificationsinput = request.POST['certificateinput']
        certifications = request.POST.getlist('certifications')
        availability_for_in_home_training = request.POST[
            'availability_for_in_home_training'] if 'availability_for_in_home_training' in request.POST else 0
        availability_for_on_line_training = request.POST[
            'availability_for_on_line_training'] if 'availability_for_on_line_training' in request.POST else 0

        name = request.POST['profile_name']
        gender = request.POST['profile_gender']
        age = request.POST['age']
        height = request.POST['height']
        weight = request.POST['weight']
        body_type = request.POST['body_type']
        profile_url = request.POST['profile_url']
        height_unit = request.POST['height_unit']
        weight_unit = request.POST['weight_unit']
        experience = request.POST['experience']
        sponser_text = request.POST['sponser_text']

        note_about_training_rates = request.POST['note_about_training_rates']
        training_methods_and_styles = request.POST['training_methods_and_styles']
        specialities = request.POST.getlist('specialities')
        languages = request.POST.getlist('languages')
        fitness_awards = request.POST['fitness_awards']
        activities = request.POST.getlist('activities')
        diet_type = request.POST['diet_type']
        prod_name_review_value = request.POST['productNameReviewValue']
        prod_review_value = request.POST['productReviewValue']
        prod_review_star_value = request.POST['productReviewStarValue']

        images_names = request.POST['sponsorImagesNameValue']
        images_names = images_names.split("','")
        images_names = images_names[0].split(',')
        

        countImages = int(request.POST['countImages'])
        
        # print(request.POST['sponsorImagesNameValues'], '------------------------posttttttttt')

        # images_values = request.FILES['sponsorImagesValueValue'] if 'sponsorImagesValueValue' in request.FILES else None
        # print(images_values)
        # images_values = images_values.split("','")
        # images_values = v[0].split(',')

        # for i in range(len(images_values)):
        #     print(images_values[i])

        profile_image = request.FILES['profile_image'] if 'profile_image' in request.FILES else None

        fitness_awards = fitness_awards.split("','")
        fitness_awards = [x.replace("'", '') for x in fitness_awards]

        certifications = ", ".join(certifications)
        specialities = ", ".join(specialities)
        languages = ", ".join(languages)
        activities = ", ".join(activities)

        prod_name_review_value = prod_name_review_value.split("','")
        prod_name_review_value = [x.replace("'", '') for x in prod_name_review_value]
        prod_review_value = prod_review_value.split("','")
        prod_review_value = [x.replace("'", '') for x in prod_review_value]
        prod_review_star_value = prod_review_star_value.split("','")
        prod_review_star_value = [x.replace("'", '') for x in prod_review_star_value]

        list_ = []
        try:
            for obj in range(len(prod_name_review_value)):
                list_.append({'name': prod_name_review_value[obj], 'review': prod_review_value[obj],
                              'star': int(prod_review_star_value[obj])})
        except:
            list_ = []

        list_ = json.dumps(list_)
        fitness_awards = json.dumps(fitness_awards)

        # fitness_awards = fitness_awards.split(',')

        fcp = FitnessProfessionalProfile.objects.get(user=user_detail)
        fcp.business_name = business_name
        fcp.degree = degree
        # fcp.brands = brands
        fcp.profession = professions
        fcp.client_preferences = client_preferences
        fcp.certifications = certifications+", "+certificationsinput
        fcp.availability_for_in_home_training = availability_for_in_home_training
        fcp.note_about_training_rates = note_about_training_rates
        fcp.training_methods_and_styles = training_methods_and_styles
        fcp.availability_for_on_line_training = availability_for_on_line_training
        fcp.specialities = specialities
        fcp.training_rates = training_rates
        fcp.fitness_awards = fitness_awards
        fcp.activities = activities
        fcp.experience = experience
        fcp.diet_type = diet_type
        fcp.product_reviews = list_


        fcp.age = age
        fcp.height = height
        fcp.height_unit = height_unit
        fcp.weight_unit = weight_unit
        fcp.weight = weight
        fcp.training_rates = training_rates
        fcp.body_type = body_type
        fcp.sponser_text = sponser_text
        fcp.languages = languages
        fcp.name = name
        user_detail.gender = gender
        user_detail.save()

        # images_names = [x.replace("'", '') for x in images_names]
        # for obj in range(len(images_names)):
        #     Professional_Sponsers.objects.create(center=fcp, sponser_name=images_names[obj])

        index = 0
        while index<=countImages:
            try:
                imgName = 'sponserImg'+str(index)
                img = request.FILES[imgName]
                Professional_Sponsers.objects.create(center=fcp, image=img)
            except:
                pass
            index+=1

        if not FitnessProfessionalProfile.objects.filter(profile_url=profile_url).exclude(id=fcp.id).exists():
            pattern = "^[A-Za-z0-9_-]*$"
            state = bool(re.match(pattern, profile_url))
            if state == True:
                fcp.profile_url = profile_url

        if profile_image:
            fcp.profile_image = profile_image

        fcp.save()

    if user_detail.active_user_role.name == FITNESS_MODAL:
        modeling_interests = request.POST.getlist('modeling_interests')
        age = request.POST['age']
        height = request.POST['height']
        weight = request.POST['weight']
        body_type = request.POST['body_type']
        height_unit = request.POST['height_unit']
        weight_unit = request.POST['weight_unit']
        eye_color = request.POST['eye_color']
        ethnicity = request.POST['ethnicity']
        tattoos = request.POST['tattoos']
        # brands = request.POST['brands']
        skin_tone = request.POST['skin_tone']
        compensation = request.POST['compensation']
        compensation_notes = request.POST['compensation_notes']
        piercing = request.POST['piercing']
        hair_length = request.POST['hair_length']
        experience = request.POST['experience']
        interested_in = request.POST.getlist('interested_in')
        about_us = request.POST['about_us']
        working_with_media = request.POST['working_with_media']
        profile_image = request.FILES['profile_image'] if 'profile_image' in request.FILES else None
        languages = request.POST.getlist('languages')

        name = request.POST['profile_name']
        gender = request.POST['profile_gender']
        profile_url = request.POST['profile_url']

        prod_name_review_value = request.POST['productNameReviewValue']
        prod_review_value = request.POST['productReviewValue']
        prod_review_star_value = request.POST['productReviewStarValue']
        languages = ", ".join(languages)
        interested_in = ", ".join(interested_in)
        modeling_interests = ", ".join(modeling_interests)

        prod_name_review_value = prod_name_review_value.split("','")
        prod_name_review_value = [x.replace("'", '') for x in prod_name_review_value]
        prod_review_value = prod_review_value.split("','")
        prod_review_value = [x.replace("'", '') for x in prod_review_value]
        prod_review_star_value = prod_review_star_value.split("','")
        prod_review_star_value = [x.replace("'", '') for x in prod_review_star_value]

        list_ = []
        try:
            for obj in range(len(prod_name_review_value)):
                list_.append({'name': prod_name_review_value[obj], 'review': prod_review_value[obj],
                              'star': int(prod_review_star_value[obj])})
        except:
            list_ = []

        list_ = json.dumps(list_)
        fcp = FitnessModalProfile.objects.get(user=user_detail)
        fcp.about_us = about_us
        fcp.modeling_interests = modeling_interests
        fcp.eye_color = eye_color
        fcp.ethnicity = ethnicity
        fcp.tattoos = tattoos
        # fcp.brands = brands
        fcp.interested_in = interested_in
        fcp.working_with_media = working_with_media
        fcp.experience = experience
        fcp.piercing = piercing
        fcp.skin_tone = skin_tone
        fcp.compensation = compensation
        fcp.c = compensation_notes
        fcp.hair_length = hair_length
        fcp.age = age
        fcp.height = height
        fcp.height_unit = height_unit
        fcp.weight_unit = weight_unit
        fcp.weight = weight
        fcp.languages = languages
        fcp.body_type = body_type
        fcp.product_reviews = list_
        fcp.name = name
        fcp.profile_url = profile_url
        user_detail.gender = gender
        user_detail.save()

        if profile_image:
            fcp.profile_image = profile_image

        fcp.save()
    messages.info(request, 'info_tab')
    return redirect('client:profile')


@ login_required
def portfolio_update(request):
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        fcp = FitnessCenterProfile.objects.get(user=user_detail)
    elif user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        fcp = FitnessProfessionalProfile.objects.get(user=user_detail)
    else:
        fcp = FitnessModalProfile.objects.get(user=user_detail)

    image_input = request.FILES['img_name']
    img_name1 = request.FILES['img_name1']
    description = request.POST['description']

    ss = SuccessStories.objects.create(
        before=image_input, description=description, after=img_name1)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        FitnessCenterProfileSuccessStories.objects.create(user=fcp, story=ss)
    elif user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        FitnessProfessionalProfileSuccessStories.objects.create(
            user=fcp, story=ss)
    else:
        FitnessModalProfileSuccessStories.objects.create(user=fcp, story=ss)
    messages.info(request, 'portfolio_tab')
    return redirect('client:profile')


@ login_required
def edit_ads_info_tab_update(request):
    user_detail = UserProfile.objects.get(user=request.user)

    identity = request.POST['id']

    if user_detail.active_user_role.name == FITNESS_CENTER:
        ad = FitnessCenterProfileAdsInformation.objects.get(id=identity)
    elif user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        ad = FitnessProfessionalAdsInformation.objects.get(id=identity)
    else:
        ad = FitnessModalProfileAdsInformation.objects.get(id=identity)

    ad = ad.ad_info

    image = request.FILES['image'] if 'image' in request.FILES else None
    session_name = request.POST['session_name'] if 'session_name' in request.POST else None
    activities = request.POST.getlist(
        'activities') if 'activities' in request.POST else None
    days = request.POST.getlist('days') if 'days' in request.POST else None
    intensity_level = request.POST['intensity_level'] if 'intensity_level' in request.POST else 0
    time = request.POST['time'] if 'time' in request.POST else ''
    location = request.POST['location'] if 'location' in request.POST else None
    description = request.POST['description'] if 'description' in request.POST else None
    price = request.POST['price'] if 'price' in request.POST else None
    spots_available = request.POST['spots_available'] if 'spots_available' in request.POST else ''

    if activities:
        activities = ", ".join(activities)
    if days:
        days = ", ".join(days)

    if image:
        ad.image = image
    if description:
        ad.description = description
    if session_name:
        ad.session_name = session_name
    if activities:
        ad.activity = activities
    if days:
        ad.days = days
    if intensity_level:
        ad.intensity_level = intensity_level
    if time:
        ad.time = time
    if location:
        ad.location = location
    if price:
        ad.price = price
    if spots_available:
        ad.spots_available = spots_available
    ad.save()

    messages.info(request, 'ads_tab')
    return redirect('client:profile')


@ login_required
def ads_info_tab_update(request):
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        fcp = FitnessCenterProfile.objects.get(user=user_detail)
    elif user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        fcp = FitnessProfessionalProfile.objects.get(user=user_detail)
    else:
        fcp = FitnessModalProfile.objects.get(user=user_detail)

    image = request.FILES['image']
    session_name = request.POST['session_name']
    activities = request.POST.getlist('activities')
    days = request.POST.getlist('days')
    intensity_level = request.POST['intensity_level'] if 'intensity_level' in request.POST else 0
    time = request.POST['time'] if 'time' in request.POST else ''
    location = request.POST['location']
    description = request.POST['description']
    price = request.POST['price']
    spots_available = request.POST['spots_available'] if 'spots_available' in request.POST else ''
    activities = ", ".join(activities)
    days = ", ".join(days)

    ad_info = AdsInformation.objects.create(image=image, description=description, session_name=session_name,
                                            activity=activities, intensity_level=intensity_level,
                                            days=days, time=time, location=location, price=price,
                                            spots_available=spots_available)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        FitnessCenterProfileAdsInformation.objects.create(
            user=fcp, ad_info=ad_info, is_remove=False)
    elif user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        FitnessProfessionalAdsInformation.objects.create(
            user=fcp, ad_info=ad_info, is_remove=False)
    else:
        FitnessModalProfileAdsInformation.objects.create(
            user=fcp, ad_info=ad_info, is_remove=False)
    messages.info(request, 'ads_tab')
    return redirect('client:profile')


def about_rating_submit(request):
    id_ = request.POST['id']
    user_detail = UserProfile.objects.get(id=int(id_))
    star = int(request.POST['star'])
    c = request.POST['comment']
    if user_detail.active_user_role.name == FITNESS_CENTER:
        fcp = FitnessCenterProfile.objects.get(user=user_detail)
        FitnessCenterRatingInput.objects.create(user=fcp, rating=star)
        rating_ = FitnessCenterRatingInput.objects.filter(
            user=fcp).aggregate(Avg('rating'))['rating__avg']
    elif user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        fcp = FitnessProfessionalProfile.objects.get(user=user_detail)
        FitnessProfessionalRatingInput.objects.create(user=fcp, rating=star)
        rating_ = FitnessProfessionalRatingInput.objects.filter(
            user=fcp).aggregate(Avg('rating'))['rating__avg']
    else:
        fcp = FitnessModalProfile.objects.get(user=user_detail)
        FitnessModalRatingInput.objects.create(user=fcp, rating=star)
        rating_ = FitnessModalRatingInput.objects.filter(
            user=fcp).aggregate(Avg('rating'))['rating__avg']

    fcp.reviews = rating_
    fcp.number_of_reviews += 1
    comm = Comments(comment=c)
    comm.save()
    fcp.comment.add(comm)
    fcp.save()

    return redirect(str(request.META['HTTP_REFERER']))


@ login_required
def portfolio_update_gallery(request):
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        fcp = FitnessCenterProfile.objects.get(user=user_detail)

        for image in request.FILES.getlist('img_name'):
            FitnessCenterGallery.objects.create(center=fcp, image=image)
    if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        fcp = FitnessProfessionalProfile.objects.get(user=user_detail)

        for image in request.FILES.getlist('img_name'):
            FitnessProfessionalsGallery.objects.create(
                center=fcp, image=image)
    if user_detail.active_user_role.name == FITNESS_MODAL:
        fcp = FitnessModalProfile.objects.get(user=user_detail)

        for image in request.FILES.getlist('img_name'):
            FitnessModalGallery.objects.create(center=fcp, image=image)
    messages.info(request, 'gallery_tab')
    return redirect('client:profile')


@ login_required
def Professional_Sponsers_Update(request):
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        fcp = FitnessProfessionalProfile.objects.get(user=user_detail)
        fcp.sponser_text = request.POST['sponser_text']
        fcp.sponsor_names = request.POST['name']
        fcp.save()
        for image in request.FILES.getlist('img_name'):
            Professional_Sponsers.objects.create(
                center=fcp, image=image)
    # messages.info(request, 'portfolio_tab')
    return redirect('client:profile')


@ login_required
def Delete_professional_Sponser(request):
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        id_ = request.POST['id']
        Professional_Sponsers.objects.filter(id=int(id_)).delete()
    # messages.info(request, 'portfolio_tab')
    return redirect('client:profile')


@ login_required
def delete_portfolio_gallery_image(request):
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        id_ = request.POST['id']
        FitnessCenterGallery.objects.filter(id=int(id_)).delete()

    if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        id_ = request.POST['id']
        FitnessProfessionalsGallery.objects.filter(id=int(id_)).delete()

    if user_detail.active_user_role.name == FITNESS_MODAL:
        id_ = request.POST['id']
        FitnessModalGallery.objects.filter(id=int(id_)).delete()
    messages.info(request, 'gallery_tab')
    return redirect('client:profile')


@ login_required
def delete_success_story(request):
    user_detail = UserProfile.objects.get(user=request.user)
    story = SuccessStories.objects.filter(id=int(request.POST['id'])).last()

    if story:
        if user_detail.active_user_role.name == FITNESS_CENTER:
            FitnessCenterProfileSuccessStories.objects.filter(
                story=story).delete()

        if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
            FitnessProfessionalProfileSuccessStories.objects.filter(
                story=story).delete()

        if user_detail.active_user_role.name == FITNESS_MODAL:
            FitnessModalProfileSuccessStories.objects.filter(
                story=story).delete()
        story.delete()
    messages.info(request, 'portfolio_tab')
    return redirect('client:profile')


@ login_required
def delete_ad_information(request):
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        id_ = request.POST['id']
        FitnessCenterProfileAdsInformation.objects.filter(
            id=int(id_)).delete()

    if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        id_ = request.POST['id']
        FitnessProfessionalAdsInformation.objects.filter(
            id=int(id_)).delete()

    if user_detail.active_user_role.name == FITNESS_MODAL:
        id_ = request.POST['id']
        FitnessModalProfileAdsInformation.objects.filter(
            id=int(id_)).delete()
    messages.info(request, 'ads_tab')
    return redirect('client:profile')


@ login_required
def update_contact_info_tab(request):
    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        fcp = FitnessCenterProfile.objects.get(user=user_detail)
    elif user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        fcp = FitnessProfessionalProfile.objects.get(user=user_detail)
    else:
        fcp = FitnessModalProfile.objects.get(user=user_detail)

    gym = request.POST['gym'] if 'gym' in request.POST else ''
    address = request.POST['address'] if 'address' in request.POST else ''
    phone_number = request.POST['phone_number']
    website = request.POST['website']
    blog_link = request.POST['blog_link']
    portal_link = request.POST['portal_link']
    facebook = request.POST['facebook']
    instagram = request.POST['instagram']
    twitter = request.POST['twitter']
    booking = request.POST['booking']
    youtube = request.POST['youtube']
    vimeo = request.POST['vimeo']
    other = request.POST['other']

    gym2 = request.POST['gym2'] if 'gym2' in request.POST else ''
    gym3 = request.POST['gym3'] if 'gym3' in request.POST else ''
    address2 = request.POST['address2'] if 'address2' in request.POST else ''
    address3 = request.POST['address3'] if 'address3' in request.POST else ''

    fcp.gym_used = gym
    fcp.gym_used2 = gym2
    fcp.gym_used3 = gym3
    fcp.phone_number = phone_number
    fcp.address = address
    fcp.website = website
    fcp.blog_link = blog_link
    fcp.portal_link = portal_link
    fcp.facebook = facebook
    fcp.instagram = instagram
    fcp.twitter = twitter
    fcp.booking_link = booking
    fcp.address2 = address2
    fcp.address3 = address3
    fcp.youtube = youtube
    fcp.vimeo_link = vimeo
    fcp.other_link = other
    fcp.save()

    messages.info(request, 'contact_tab')

    return redirect('client:profile')


@ login_required
def top_bar_info_update(request):
    user_detail = UserProfile.objects.get(user=request.user)
    gender_ = request.POST['gender'] if 'gender' in request.POST else None
    if gender_:
        user_detail.gender = gender_
    user_detail.save()
    if user_detail.active_user_role.name == FITNESS_CENTER:
        open_since = request.POST['open_since']
        name = request.POST['name']
        profile_url = request.POST['profile_url']
        fitness_center = request.POST['fitness_center']

        profile_url = profile_url.lower()

        fcp = FitnessCenterProfile.objects.get(user=user_detail)
        fcp.open_since = open_since
        fcp.name = name
        fcp.fitness_center_type = FitnessCenterType.objects.get(
            id=int(fitness_center))

        if not FitnessCenterProfile.objects.filter(profile_url=profile_url).exclude(id=fcp.id).exists():
            pattern = "^[A-Za-z0-9_-]*$"
            state = bool(re.match(pattern, profile_url))
            if state == True:
                fcp.profile_url = profile_url
            else:
                messages.info(request, 'Select Role to complete registration')
                return redirect('client:profile')
        else:
            messages.error(request, 'Ooops! This url is already taken')
        fcp.save()

    if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        age = request.POST['age']
        name = request.POST['name']
        height = request.POST['height']
        weight = request.POST['weight']
        training_rates = request.POST['training_rates']
        experience = request.POST['experience']
        body_type = request.POST['body_type']
        profile_url = request.POST['profile_url']
        height_unit = request.POST['height_unit']
        weight_unit = request.POST['weight_unit']

        languages = request.POST.getlist('languages')
        languages = ", ".join(languages)

        fcp = FitnessProfessionalProfile.objects.get(user=user_detail)
        fcp.age = age
        fcp.name = name
        fcp.height = height
        fcp.height_unit = height_unit
        fcp.weight_unit = weight_unit
        fcp.weight = weight
        fcp.training_rates = training_rates
        fcp.experience = experience
        fcp.body_type = body_type
        fcp.languages = languages

        if not FitnessProfessionalProfile.objects.filter(profile_url=profile_url).exclude(id=fcp.id).exists():
            pattern = "^[A-Za-z0-9_-]*$"
            state = bool(re.match(pattern, profile_url))
            if state == True:
                fcp.profile_url = profile_url
            else:
                messages.info(request, 'Select Role to complete registration')
                return redirect('client:profile')
        else:
            messages.error(request, 'Ooops! This url is already taken')
        fcp.save()

    if user_detail.active_user_role.name == FITNESS_MODAL:
        age = request.POST['age']
        name = request.POST['name']
        height = request.POST['height']
        weight = request.POST['weight']
        compensation = request.POST['compensation']
        experience = request.POST['experience']
        body_type = request.POST['body_type']
        profile_url = request.POST['profile_url']
        height_unit = request.POST['height_unit']
        weight_unit = request.POST['weight_unit']

        languages = request.POST.getlist('languages')
        languages = ", ".join(languages)

        fcp = FitnessModalProfile.objects.get(user=user_detail)
        fcp.age = age
        fcp.name = name
        fcp.height = height
        fcp.weight = weight
        fcp.height_unit = height_unit
        fcp.weight_unit = weight_unit
        fcp.compensation = compensation
        fcp.experience = experience
        fcp.body_type = body_type
        fcp.languages = languages

        if not FitnessModalProfile.objects.filter(profile_url=profile_url).exclude(id=fcp.id).exists():
            pattern = "^[A-Za-z0-9_-]*$"
            state = bool(re.match(pattern, profile_url))
            if state == True:
                fcp.profile_url = profile_url
            else:
                messages.info(request, 'Select Role to complete registration')
                return redirect('client:profile')
        else:
            messages.error(request, 'Ooops! This url is already taken')
        fcp.save()

    return redirect('client:profile')

def heart_counter(request):
    user_id = request.POST['user_id']
    visitor_id = request.session['visitor_id']
    heart = Heart_Modal.objects.filter(user = user_id , user_session = visitor_id)
    if not heart:
        heart = Heart_Modal.objects.create(user = user_id, user_session = visitor_id, hearts_counter = 1)
        heart.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def blog_heart_counter(request):
    blog_id_ = request.POST['blog_id']
    heart = Blog_Heart_Modal.objects.create(blog_id = int(blog_id_), hearts_counter = 1)
    heart.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def delete_video_link_pro(request):
    id = request.POST['id']
    id_ = int(id)

    user_detail = UserProfile.objects.get(user=request.user)

    if user_detail.active_user_role.name == FITNESS_CENTER:
        try:
            getObj = FitnessCenterYoutubeVideoLinks.objects.get(id=id_)
            getObj.delete()
        except:
            pass
    if user_detail.active_user_role.name == FITNESS_PROFESSIONAL:
        try:
            getObj = FitnessProfessionalYoutubeVideoLinks.objects.get(id=id_)
            getObj.delete()
        except:
            pass
    
    if user_detail.active_user_role.name == FITNESS_MODAL:
        try:
            getObj = FitnessModelYoutubeVideoLinks.objects.get(id=id_)
            getObj.delete()
        except:
            pass
    return redirect('/accounts/details')

# user, created = User.objects.get_or_create(
#                 username=email, email=email)
#             if not created:
#                 messages.error(
#                     request, 'This email address is already registered')
#                 return render(request, 'client/accounts/signup.html', context=context)