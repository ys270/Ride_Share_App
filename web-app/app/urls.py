from django.urls import path

from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('index/', views.index, name='index'),
    path('request_ride/', views.request_ride, name='request_ride'),
    path('join_ride/',views.join_ride,name='join_ride'),
    path('my_rides_as_sharer/', views.my_rides_as_sharer, name='my_rides_as_sharer'),
    path('my_rides_as_owner/',views.my_rides_as_owner,name='my_rides_as_owner'),
    path('my_rides_as_driver/',views.my_rides_as_driver,name='my_rides_as_driver'),
    path('select_sharer_ride/',views.select_sharer_ride,name='select_sharer_ride'),
    path('owner_open/',views.owner_open,name='owner_open'),
    path('owner_open_detail/',views.owner_open_detail,name='owner_open_detail'),
    path('owner_edit_fail/',views.owner_edit_fail,name='owner_edit_fail'),
    path('owner_confirmed/',views.owner_confirmed,name='owner_confirmed'),
    path('owner_confirmed_detail/',views.owner_confirmed_detail,name='owner_confirmed_detail'),
    path('my_rides_as_sharer/',views.my_rides_as_sharer,name='my_rides_as_sharer'),
    path('my_rides_as_sharer/',views.my_rides_as_sharer,name='my_rides_as_sharer'),
    path('sharer_confirmed/',views.sharer_confirmed,name='sharer_confirmed'),
    path('sharer_confirmed_detail/',views.sharer_confirmed_detail,name='sharer_confirmed_detail'),
    path('sharer_open/',views.sharer_open,name='sharer_open'),
    path('sharer_quit/',views.sharer_quit,name='sharer_quit'),
    path('register_as_driver/',views.register_as_driver,name='register_as_driver'),
    path('edit_driver_information/',views.edit_driver_information,name='edit_driver_information'),
    path('driver_search/',views.driver_search,name='driver_search'),
    path('request_ride_success/', views.request_ride_success, name='request_ride_success'),
    path('join_ride_success/', views.join_ride_success, name='join_ride_success'),
    path('driver_ride_detail/', views.driver_ride_detail, name='driver_ride_detail'),

]
