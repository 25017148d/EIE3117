from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
    )
    nickname = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=USER_TYPE_CHOICES)
    profile_image = models.TextField(blank=True, null=True)


class Route(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_routes')
    date = models.DateField()
    time = models.TimeField()
    start_location = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)
    car_model = models.CharField(max_length=128)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    passengers = models.ManyToManyField(User, through='Booking', related_name='booked_routes')
    created_at = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['route', 'passenger'], name='unique_route_passenger')
        ]
