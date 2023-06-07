from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Review, Tag
from .form import ProjectForm, ReviewForm
from .searchbar import searchbar, changingpage


def projects(request):
    projects , search_query = searchbar(request)
    projects, custom_range = changingpage(request, projects)


    content = {'list' : projects, 'custom_range': custom_range , 'search_query': search_query}
    return render(request, 'projects/h1.html', content)

def sproject(request, pk):
    single = Project.objects.get(id= pk)
    tag = single.tags.all()

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        commenter = form.save(commit=False)
        commenter.project = single
        commenter.owner = request.user.profile
        commenter.save()
        messages.success(request, 'your review add successfully')

        single.getVoteCount
        
        return redirect('sproject', pk =single.id)

    content = {'part':single, 'tag' : tag, 'form': form}
    return render(request, 'projects/p.html', content)

@login_required(login_url='login')
def creatProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':

        form = ProjectForm(request.POST, request.FILES)
        newTags = request.POST.get('newtags').replace(',', " ").split()
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            messages.success(request, 'Project Added')
            project.save()

            for tag in newTags:
                ntag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(ntag)
            
            return redirect('projects')

    return render(request, 'projects/formmaker.html', {'form': form})

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    proj = profile.project_set.get(id = pk)
    form = ProjectForm(instance=proj)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=proj)
        newTags = request.POST.get('newtags').replace(',', " ").split()
        if form.is_valid():
            proj = form.save()

            for tag in newTags:
                ntag, created = Tag.objects.get_or_create(name=tag)
                proj.tags.add(ntag)

            return redirect('account')

    return render(request, 'projects/formmaker.html', {'form': form, 'project': proj})

@login_required(login_url='login')
def deletProject(request, pk):
    profile = request.user.profile
    proj = profile.project_set.get(id= pk)

    if request.method == 'POST':
        proj.delete()
        return redirect('projects')
        
    context = {'obj': proj}
    return render(request, 'DeletForm.html', context)