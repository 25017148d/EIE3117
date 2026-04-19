from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Route, Booking


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

    def validate_profileImage(self, value):
        # Reject suspicious data URIs or very large payloads to avoid abuse
        if not value:
            return value
        low = value.lower()
        if 'data:text/html' in low or '<script' in low or 'javascript:' in low:
            raise serializers.ValidationError('Invalid profile image')
        if len(value) > 200000:
            raise serializers.ValidationError('Profile image too large')
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
    passengers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
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
            'description',
            'passengers',
            'passengerDetails'
        ]

    def get_passengerDetails(self, obj):
        passengers = obj.passengers.all()
        return UserPublicSerializer(passengers, many=True).data

    # Basic input validators to reduce risk of stored XSS / SSTI-like payloads
    def _reject_bad(self, value):
        if value is None:
            return value
        bad_substrings = ['<script', '</script>', '{{', '}}', '{%', '%}', 'javascript:', 'onerror=', 'onload=']
        low = value.lower()
        for bad in bad_substrings:
            if bad in low:
                raise serializers.ValidationError('Invalid characters in input')
        return value

    def validate_startLocation(self, value):
        return self._reject_bad(value)

    def validate_destination(self, value):
        return self._reject_bad(value)

    def validate_carModel(self, value):
        return self._reject_bad(value)

    def validate_description(self, value):
        # Keep description length bounded and reject dangerous snippets
        if value and len(value) > 2000:
            raise serializers.ValidationError('Description too long')
        return self._reject_bad(value)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'route', 'passenger', 'created_at']
