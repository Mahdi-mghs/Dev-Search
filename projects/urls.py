from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('test/<str:pk>', views.sproject, name='sproject'),
    path('create-project', views.creatProject, name='create-project'),
    path('update-pr/<str:pk>', views.updateProject, name='update-pr'),
    path('del-pr/<str:pk>', views.deletProject, name='del-pr'),
]