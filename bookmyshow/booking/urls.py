from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from booking.views import *

urlpatterns = [
    url(r'^movie/put/', put_movie, name='movie_create'),
    url(r'^theatre/put/', put_theatre, name='theatre_create'),
    url(r'^screen/put/', put_screen, name='screen_create'),
    url(r'^show/put/', put_show, name='show_create'),
    url(r'^seat/put/', put_seat, name='seat_create'),
    url(r'^book/$', book, name='book_create'),
    url(r'^book/get', get_booking, name='book_get'),
]
