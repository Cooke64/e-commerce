from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('signup/', views.signup, name='signup'),
    path('user_profile/', views.user_profile, name='user_profile'),
]
