from django.contrib import admin
from .models import CarCategory, Car, Booking

@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rate_per_day', 'is_available')
    list_filter = ('is_available', 'category')
    search_fields = ('name', 'features')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'user', 'pickup_date', 'drop_date', 'status', 'total_amount')
    list_filter = ('status', 'pickup_date')
    search_fields = ('car__name', 'user__username')