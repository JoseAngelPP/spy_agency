from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django import views as django_views
from hits.views import *


app_name = 'hits'

urlpatterns = [
    path('', login_required(ListHitsView.as_view()), name='hits_list'),
    path('create/', login_required(CreateHitView.as_view()), name='create_hit'),
    path('<int:pk>/', login_required(UpdateHitView.as_view()), name='detail_hit'),
    # path('<int:pk>/edit/', login_required(UpdateHitView.as_view()), name='update_hit'),
]