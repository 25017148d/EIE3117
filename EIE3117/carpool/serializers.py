from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Route, Booking
import os
from urllib.parse import urlparse


User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'loginId', 'nickname', 'email', 'type', 'profileImage']

    loginId = serializers.CharField(source='username')
    profileImage = serializers.CharField(source='profile_image', allow_null=True, required=False)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    loginId = serializers.CharField(source='username')
    profileImage = serializers.CharField(source='profile_image', allow_null=True, required=False)

    class Meta:
        model = User
        fields = ['loginId', 'nickname', 'email', 'type', 'profileImage', 'password', 'password2']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'password2': 'Passwords do not match'})
        return attrs

    def validate_profile_image(self, value):
        if not value:
            return value

        # Only allow data: image URIs or https URLs from trusted domains.
        allowed_data_prefixes = (
            'data:image/png;base64,',
            'data:image/jpeg;base64,',
            'data:image/jpg;base64,',
            'data:image/gif;base64,',
            'data:image/webp;base64,',
        )
        if any(value.startswith(p) for p in allowed_data_prefixes):
            if len(value) > 2_000_000:
                raise serializers.ValidationError('Profile image is too large')
            return value

        # If it's an http(s) URL, validate domain against TRUSTED_IMAGE_DOMAINS env var
        parsed = urlparse(value)
        if parsed.scheme not in ('https', 'http') or not parsed.netloc:
            raise serializers.ValidationError('Profile image must be a data URI or an https URL')

        trusted = os.environ.get('TRUSTED_IMAGE_DOMAINS')
        if not trusted:
            # By default, disallow external http URLs to avoid SSRF/abuse unless explicitly configured
            raise serializers.ValidationError('External image URLs are not allowed (no TRUSTED_IMAGE_DOMAINS configured)')

        trusted_domains = [d.strip().lower() for d in trusted.split(',') if d.strip()]
        host = parsed.netloc.lower()
        if not any(host == td or host.endswith('.' + td) for td in trusted_domains):
            raise serializers.ValidationError('Image host is not in the trusted domains list')

        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2', None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class RouteSerializer(serializers.ModelSerializer):
    driverId = serializers.CharField(source='driver_id', read_only=True)
    driverName = serializers.CharField(source='driver.nickname', read_only=True)
    driverAvatar = serializers.CharField(source='driver.profile_image', allow_null=True, read_only=True)
    startLocation = serializers.CharField(source='start_location')
    destination = serializers.CharField()
    carModel = serializers.CharField(source='car_model')
    totalSeats = serializers.IntegerField(source='total_seats')
    availableSeats = serializers.IntegerField(source='available_seats', read_only=True)
    isBooked = serializers.SerializerMethodField()
    passengers = serializers.SerializerMethodField()
    passengerDetails = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = [
            'id',
            'driverId',
            'driverName',
            'driverAvatar',
            'date',
            'time',
            'startLocation',
            'destination',
            'carModel',
            'totalSeats',
            'availableSeats',
            'isBooked',
            'description',
            'passengers',
            'passengerDetails'
        ]

    def _can_view_passengers(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        return bool(user and user.is_authenticated and (user.is_staff or obj.driver_id == user.id))

    def get_isBooked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        if getattr(obj, 'is_booked', None) is not None:
            return bool(obj.is_booked)
        return Booking.objects.filter(route=obj, passenger=user).exists()

    def get_passengers(self, obj):
        if not self._can_view_passengers(obj):
            return []
        return list(obj.passengers.values_list('id', flat=True))

    def get_passengerDetails(self, obj):
        if not self._can_view_passengers(obj):
            return []
        passengers = obj.passengers.all()
        return UserPublicSerializer(passengers, many=True).data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'route', 'passenger', 'created_at']
