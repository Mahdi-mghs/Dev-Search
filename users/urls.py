from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginUser, name='login'),
    path('logout/', views.logoutUser,name='logout'),
    path('register/', views.register, name='register'),


    path('account/', views.userPage, name='account'),
    path('acc-form/',views.accountForm, name='accform'),
    path('', views.profile, name='profile'),
    path('profile/<str:pk>/', views.skillPf, name='single-pf'),

    path('skillform/' , views.skillform, name='skillform'),
    path('update-skillform/<str:pk>/' , views.updateskill, name='updateskill'),
    path('delete-skillform/<str:pk>/' , views.delskill, name='deleteskill'),

    path('inbox/', views.message, name='inbox'),
    path('message/<str:pk>/', views.singlemessage, name='message'),
    path('messageform/<str:pk>/', views.messageform, name='messform')
]