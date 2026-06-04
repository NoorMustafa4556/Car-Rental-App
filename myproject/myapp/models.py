from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class CarCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CarCategory, self).save(*args, **kwargs)


class Car(models.Model):
    category = models.ForeignKey(CarCategory, related_name='cars', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    rate_per_day = models.FloatField(null=True)
    description = models.TextField(null=True, blank=True)
    features = models.CharField(max_length=500, null=True, blank=True, help_text="Comma separated features e.g. AC, Auto, 4 Seats")
    image = models.ImageField(upload_to='cars/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    pickup_date = models.DateField(null=True)
    drop_date = models.DateField(null=True)
    pickup_location = models.CharField(max_length=300, null=True)
    drop_location = models.CharField(max_length=300, null=True)
    total_amount = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_booked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.car.name}"
