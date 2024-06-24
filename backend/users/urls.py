from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyUserViewSet

app_name = 'users'

router = DefaultRouter()

router.register('users', MyUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    # path('users/', MyUserViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('users/<int:id>/', MyUserViewSet.as_view({'get': 'retrieve'})),
    path('', include('djoser.urls')),
    # path('users/me/avatar/', MyUserViewSet.as_view(
    #     {'put': 'partial_update', 'delete': 'partial_update'})),
    path('auth/', include('djoser.urls.authtoken')),
]
