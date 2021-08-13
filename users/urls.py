from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django import views as django_views
from users.views import *


app_name = 'users'

urlpatterns = [
    path('', login_required(HomeView.as_view()), name='home'),
    path('login/', LoginView.as_view(success_url='/hits'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CreateCustomUserView.as_view(), name='create_user'),
    path('hitmen/', login_required(ListHitmenView.as_view()), name='hitmen_list'),
    path('hitmen/<int:pk>/', login_required(UpdateCustomUserView.as_view()), name='detail_user'),
    # path('hitmen/<int:pk>/edit/', login_required(UpdateCustomUserView.as_view()), name='update_user'),
    
]