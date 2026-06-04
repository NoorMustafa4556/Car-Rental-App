from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Custom Admin URLs
    path('dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('dashboard/cars/', views.custom_admin_cars, name='custom_admin_cars'),
    path('dashboard/cars/add/', views.custom_admin_add_car, name='custom_admin_add_car'),
    path('dashboard/cars/edit/<int:pk>/', views.custom_admin_edit_car, name='custom_admin_edit_car'),
    path('dashboard/cars/delete/<int:pk>/', views.custom_admin_delete_car, name='custom_admin_delete_car'),
    path('dashboard/bookings/', views.custom_admin_bookings, name='custom_admin_bookings'),
    path('dashboard/bookings/update/<int:pk>/', views.custom_admin_update_booking, name='custom_admin_update_booking'),
]