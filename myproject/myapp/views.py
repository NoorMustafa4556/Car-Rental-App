from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from .models import Car, Booking, CarCategory
from datetime import datetime

# --- PUBLIC VIEWS ---

def home(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'home.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        pickup_date_str = request.POST.get('pickup_date')
        drop_date_str = request.POST.get('drop_date')
        pickup_location = request.POST.get('pickup_location')
        drop_location = request.POST.get('drop_location')
        
        pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date()
        drop_date = datetime.strptime(drop_date_str, '%Y-%m-%d').date()
        
        days = (drop_date - pickup_date).days
        if days <= 0:
            days = 1
            
        total_amount = days * car.rate_per_day
        
        Booking.objects.create(
            user=request.user,
            car=car,
            pickup_date=pickup_date,
            drop_date=drop_date,
            pickup_location=pickup_location,
            drop_location=drop_location,
            total_amount=total_amount,
            status='Pending'
        )
        return redirect('my_bookings')
        
    return render(request, 'car_detail.html', {'car': car})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date_booked')
    return render(request, 'my_bookings.html', {'bookings': bookings})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- CUSTOM ADMIN VIEWS ---

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'category', 'rate_per_day', 'description', 'features', 'image', 'is_available']

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def custom_admin_dashboard(request):
    context = {
        'total_cars': Car.objects.count(),
        'total_bookings': Booking.objects.count(),
        'confirmed_bookings': Booking.objects.filter(status='Confirmed').count(),
        'pending_bookings': Booking.objects.filter(status='Pending').count(),
        'recent_bookings': Booking.objects.order_by('-date_booked')[:5],
    }
    return render(request, 'custom_admin/dashboard.html', context)

@user_passes_test(is_admin)
def custom_admin_cars(request):
    cars = Car.objects.all().order_by('-id')
    return render(request, 'custom_admin/cars.html', {'cars': cars})

@user_passes_test(is_admin)
def custom_admin_add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('custom_admin_cars')
    else:
        form = CarForm()
    return render(request, 'custom_admin/car_form.html', {'form': form})

@user_passes_test(is_admin)
def custom_admin_edit_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('custom_admin_cars')
    else:
        form = CarForm(instance=car)
    return render(request, 'custom_admin/car_form.html', {'form': form})

@user_passes_test(is_admin)
def custom_admin_delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('custom_admin_cars')

@user_passes_test(is_admin)
def custom_admin_bookings(request):
    bookings = Booking.objects.all().order_by('-date_booked')
    return render(request, 'custom_admin/bookings.html', {'bookings': bookings})

@user_passes_test(is_admin)
def custom_admin_update_booking(request, pk):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
    return redirect('custom_admin_bookings')