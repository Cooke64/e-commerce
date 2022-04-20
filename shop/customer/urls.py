from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('signup/', views.signup, name='signup'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_user_account/', views.delete_user_account, name='delete_user_account'),
    path('confirm/', views.enter_code_to_confirm, name='confirm'),
    path('unsubscribe/', views.stop_user_being_subscribed, name='unsubscribe'),
]
