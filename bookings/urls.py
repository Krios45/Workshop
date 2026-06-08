from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_list, name='list'),
    path('create/<int:asset_id>/', views.booking_create, name='create'),
    path('<int:pk>/approve/', views.booking_approve, name='approve'),
    path('<int:pk>/reject/', views.booking_reject, name='reject'),
    path('<int:pk>/return/', views.booking_return, name='return'),
    path('<int:pk>/cancel/', views.booking_cancel, name='cancel'),
]
