
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import RegisterUserViewSet,LogoutAPIView,TokenObtainPairPatchedView,UserDetailViewSet



urlpatterns = [
    path('login', TokenObtainPairPatchedView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('register', RegisterUserViewSet.as_view({'post': 'create'}), name='register'),
    path('logout', LogoutAPIView.as_view(), name='auth-logout'),
    path('user', UserDetailViewSet.as_view({'get': 'retrieve'}), name='user'),
    path('all-user', UserDetailViewSet.as_view({'get': 'list'}), name='all-user'),
]
