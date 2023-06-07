from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .searchbar import searchbar, changingpage
from .models import Profile
from .form import UserFormRegister, UpdateForm, SkillForm, MessageForm


# Create your views here.
def loginUser(request):

    if request.user.is_authenticated:
        return redirect('profile')


    if request.method == 'POST':
        uname = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username = uname)
        except:
            messages.error(request ,"username doesn't match!")

        user = authenticate(request, username=uname, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request ,'Username or Password are incorrect!')
    return render(request, 'users/login-register.html')

def logoutUser(request):
    messages.info(request ,'User exited!')
    logout(request)
    return redirect('login')

def register(request):
    page = 'register'
    form = UserFormRegister()
    if request.method == 'POST':
        form = UserFormRegister(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User successfully Added!')
            
            login(request, user)
            return redirect('accform')
        else:
            messages.error(
                request, 'An Error occurred !')

    context = {'page': page, 'form': form}
    return render(request, 'users/login-register.html', context)

def profile(request):

    profiles, search_query = searchbar(request)
    profiles, custom_range = changingpage(request, profiles)

    context = {'profiles' : profiles, 'search_queary' : search_query, 'custom_range': custom_range}
    return render(request, 'users/profile.html', context)

def skillPf(request, pk):
    Sproject = Profile.objects.get(id = pk)
    toptags = Sproject.skill_set.exclude(desc="")
    othertags = Sproject.skill_set.filter(desc="")
    context = {'profile' : Sproject, 'othertags' : othertags, 'toptags': toptags}
    return render(request, 'users/user-pf.html', context)


@login_required(login_url = 'login')
def userPage(request):
    profile = request.user.profile
    tags = profile.skill_set.all()
    proj = profile.project_set.all()
    context = {'profile': profile, 'tags': tags, 'proj': proj}
    return render(request, 'users/account.html', context)

@login_required(login_url = 'login')
def accountForm(request):
    profile = request.user.profile
    form = UpdateForm(instance=profile)
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

            
    context = {'form': form}
    return render(request ,'users/acc-form.html', context)

@login_required(login_url = 'login')
def skillform(request):
    form = SkillForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url = 'login')
def updateskill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id = pk)
    form = SkillForm(instance =skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance = skill)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)

@login_required(login_url='login')
def delskill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id = pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')

    context = {'obj': skill}
    return render(request, 'DeletForm.html', context)

@login_required(login_url='login')
def message(request):

    profile = request.user.profile
    messageOwner = profile.messages.all()
    unreadCount = messageOwner.filter(is_read=False).count()

    context = {'messageOwner':messageOwner, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)

def singlemessage(request, pk):

    profile = request.user.profile
    single_message = profile.messages.get(id=pk)
    single_message.is_read = True
    single_message.save()

    context = {'mess': single_message}
    return render(request, 'users/message.html', context)

def messageform(request, pk):

    reciver = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None


    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            mess = form.save(commit=False)
            mess.sender = sender
            mess.reciver = reciver

            if sender:
                mess.name = sender.name 
                mess.email = sender.email
            mess.save()

            messages.success(request, 'message sent successfully')
            return redirect('single-pf', pk =reciver.id)

    context = {'recipest': reciver, 'form': form}
    return render(request, 'users/message-form.html', context)