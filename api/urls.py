from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projectsapi/', views.getProjects),
    path('projectapi/<str:pk>', views.getProject),
    path('projectapi/<str:pk>/vote/', views.getProjectVote),

    path('remove-tag/', views.delTags)
]