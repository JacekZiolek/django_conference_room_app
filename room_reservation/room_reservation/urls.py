"""
URL configuration for room_reservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from room_reservation_app.views import Main, AddRoom, RoomList, DeleteRoom, EditRoom, BookRoom, RoomDetails

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.as_view()),
    path('room/new/', AddRoom.as_view()),
    path('rooms/', RoomList.as_view()),
    path('room/delete/<int:room_id>/', DeleteRoom.as_view()),
    path('room/modify/<int:room_id>/', EditRoom.as_view()),
    path('room/book/<int:room_id>/', BookRoom.as_view()),
    path('room/details/<int:room_id>/', RoomDetails.as_view()),
]
