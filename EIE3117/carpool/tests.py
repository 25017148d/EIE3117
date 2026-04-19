from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from .models import Booking, Route


User = get_user_model()


class RouteSecurityTests(APITestCase):
	def setUp(self):
		self.driver = User.objects.create_user(
			username='driver1',
			password='StrongPass123!',
			nickname='Driver One',
			email='driver1@example.com',
			type='driver',
		)
		self.passenger = User.objects.create_user(
			username='passenger1',
			password='StrongPass123!',
			nickname='Passenger One',
			email='passenger1@example.com',
			type='passenger',
		)
		self.route = Route.objects.create(
			driver=self.driver,
			date='2026-04-20',
			time='09:30',
			start_location='Campus',
			destination='City Center',
			car_model='Toyota Camry',
			total_seats=3,
			available_seats=2,
			description='Morning commute',
		)
		Booking.objects.create(route=self.route, passenger=self.passenger)

	def auth_client(self, user):
		token = RefreshToken.for_user(user).access_token
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

	def test_public_route_list_redacts_passengers(self):
		response = self.client.get('/api/routes/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data[0]['passengers'], [])
		self.assertEqual(response.data[0]['passengerDetails'], [])
		self.assertFalse(response.data[0]['isBooked'])

	def test_booked_route_marks_is_booked_for_authenticated_passenger(self):
		self.auth_client(self.passenger)

		response = self.client.get(f'/api/routes/{self.route.id}/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(response.data['isBooked'])
		self.assertEqual(response.data['passengers'], [])
		self.assertEqual(response.data['passengerDetails'], [])

	def test_route_owner_can_view_passenger_details(self):
		self.auth_client(self.driver)

		response = self.client.get(f'/api/routes/{self.route.id}/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['passengers'], [self.passenger.id])
		self.assertEqual(response.data['passengerDetails'][0]['nickname'], self.passenger.nickname)

	def test_profile_image_validation_rejects_unsafe_scheme(self):
		response = self.client.post('/api/auth/register/', {
			'loginId': 'newuser',
			'nickname': 'New User',
			'email': 'new@example.com',
			'type': 'passenger',
			'profileImage': 'javascript:alert(1)',
			'password': 'StrongPass123!',
			'password2': 'StrongPass123!',
		}, format='json')

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('profileImage', response.data)
