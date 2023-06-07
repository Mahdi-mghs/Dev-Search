from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def changingpage(request, projects):
    page = request.GET.get('page')

    paginate = Paginator(projects, 6)
    try:
        projects = paginate.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginate.page(page)
    except EmptyPage:
        page = paginate.num_pages
        projects = paginate.page(page)

    leftindex = int(page) - 2
    if leftindex < 1:
        leftindex = 1

    rightindex = int(page) + 3

    if rightindex > paginate.num_pages:
        rightindex = paginate.num_pages + 1

    custom_range = range(leftindex, rightindex)

    return projects, custom_range 

def searchbar(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains = search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_query) |
        Q(owner__name__icontains = search_query) |
        Q(tags__in= tags)
    )

    return projects, search_query