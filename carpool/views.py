from django.db import transaction
import os
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Route, Booking
from .serializers import UserRegisterSerializer, UserPublicSerializer, RouteSerializer


User = get_user_model()


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserPublicSerializer(user).data, status=status.HTTP_201_CREATED)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserPublicSerializer(request.user).data)


class HealthAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'status': 'ok'})


class TokenObtainPairCookieView(TokenObtainPairView):
    """Obtain JWT pair but set refresh token as HttpOnly cookie.

    Returns only the `access` in the JSON body and stores `refresh` in a secure HttpOnly cookie.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # If token pair issued, move refresh into HttpOnly cookie and return only access in body
        if response.status_code == 200 and isinstance(response.data, dict) and 'refresh' in response.data:
            refresh = response.data.get('refresh')
            access = response.data.get('access')
            resp = Response({'access': access}, status=response.status_code)
            secure_flag = not (os.environ.get('DEBUG', 'True') == 'True')
            # keep refresh cookie lifetime reasonably long (backend SIMPLE_JWT controls actual lifetime)
            max_age = 7 * 24 * 60 * 60
            resp.set_cookie('refresh', refresh, httponly=True, secure=secure_flag, samesite='Lax', max_age=max_age)
            return resp
        return response


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.select_related('driver').prefetch_related('passengers').all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if self.request.user.type != 'driver':
            raise PermissionDenied('Only drivers can publish routes')
        serializer.save(driver=self.request.user, available_seats=serializer.validated_data['total_seats'])

    def perform_update(self, serializer):
        route = self.get_object()
        if self.request.user.type != 'driver':
            raise PermissionDenied('Only drivers can manage routes')
        if route.driver_id != self.request.user.id:
            raise PermissionDenied('Only the route owner can manage this route')
        booked_count = Booking.objects.filter(route=route).count()
        total_seats = serializer.validated_data.get('total_seats', route.total_seats)
        if total_seats < booked_count:
            raise PermissionDenied('Total seats cannot be less than booked seats')
        serializer.save(available_seats=total_seats - booked_count)

    def perform_destroy(self, instance):
        if self.request.user.type != 'driver':
            raise PermissionDenied('Only drivers can manage routes')
        if instance.driver_id != self.request.user.id:
            raise PermissionDenied('Only the route owner can manage this route')
        if Booking.objects.filter(route=instance).exists():
            raise PermissionDenied('Cannot delete a route with active bookings')
        instance.delete()

    @action(detail=False, methods=['get'], url_path='my-routes', permission_classes=[IsAuthenticated])
    def my_routes(self, request):
        routes = self.get_queryset().filter(driver=request.user)
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my-bookings', permission_classes=[IsAuthenticated])
    def my_bookings(self, request):
        routes = self.get_queryset().filter(passengers=request.user)
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'], url_path='book', permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        route = self.get_object()
        if request.user.type != 'passenger':
            return Response({'detail': 'Only passengers can book routes'}, status=status.HTTP_403_FORBIDDEN)

        if request.method.lower() == 'post':
            with transaction.atomic():
                route = Route.objects.select_for_update().get(pk=route.pk)
                if route.available_seats <= 0:
                    return Response({'detail': 'No seats available'}, status=status.HTTP_400_BAD_REQUEST)
                if Booking.objects.filter(route=route, passenger=request.user).exists():
                    return Response({'detail': 'You already booked this route'}, status=status.HTTP_400_BAD_REQUEST)
                Booking.objects.create(route=route, passenger=request.user)
                route.available_seats -= 1
                route.save(update_fields=['available_seats'])
            serializer = self.get_serializer(route)
            return Response(serializer.data)

        with transaction.atomic():
            route = Route.objects.select_for_update().get(pk=route.pk)
            deleted, _ = Booking.objects.filter(route=route, passenger=request.user).delete()
            if deleted == 0:
                return Response({'detail': 'Booking not found'}, status=status.HTTP_400_BAD_REQUEST)
            route.available_seats += 1
            route.save(update_fields=['available_seats'])
        serializer = self.get_serializer(route)
        return Response(serializer.data)
