from .models import Profile, Skill
from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def changingpage(request, profiles):
    page = request.GET.get('page')

    paginate = Paginator(profiles, 2)
    try:
        profiles = paginate.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginate.page(page)
    except EmptyPage:
        page = paginate.num_pages
        profiles = paginate.page(page)

    leftindex = int(page) - 2
    if leftindex < 1:
        leftindex = 1

    rightindex = int(page) + 3

    if rightindex > paginate.num_pages:
        rightindex = paginate.num_pages + 1

    custom_range = range(leftindex, rightindex)

    return profiles, custom_range 

def searchbar(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains = search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains = search_query) |
        Q(short_intro__icontains = search_query) |
        Q(skill__in= skills)
    )

    return profiles, search_query