"""
URL configuration for badminton project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import index, add_player, view_players, start_tournament, next_round, reset_tournament
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('add-player/', add_player, name='add_player'),
    path('view-players/', view_players, name='view_players'),
    path('start-tournament/', start_tournament, name='start_tournament'),
    path('next-round/', next_round, name='next_round'),
    path('reset-tournament/', reset_tournament, name='reset_tournament'),
]
