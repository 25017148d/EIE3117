from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Route, Booking


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'type', 'profile_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname', 'type', 'profile_image')}),
    )


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'date', 'time', 'start_location', 'destination', 'available_seats')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'passenger', 'created_at')
