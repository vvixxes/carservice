from django.urls import path
from . import views


urlpatterns = [
    path('', views.book_repair, name='book_repair'),
    path('schedule/', views.schedule, name='schedule'),
]