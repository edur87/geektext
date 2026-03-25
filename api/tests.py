from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, CreditCard


class ProfileManagementAPITests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="johndoe",
			password="SecurePassword123!",
			email="john@example.com",
			name="John Doe",
			home_address="123 Main St",
		)

	def test_users_endpoint_get_is_browsable(self):
		response = self.client.get(reverse("create_user"))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("supported_methods", response.data)

	def test_create_user_returns_public_profile_data(self):
		response = self.client.post(
			reverse("create_user"),
			{
				"username": "janedoe",
				"password": "SecurePassword456!",
				"email": "jane@example.com",
				"name": "Jane Doe",
				"home_address": "456 Oak Ave",
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["username"], "janedoe")
		self.assertNotIn("password", response.data)
		self.assertIn("id", response.data)

	def test_get_user_returns_credit_cards_with_masked_number(self):
		CreditCard.objects.create(
			user=self.user,
			card_number="4532015112830366",
			cardholder_name="John Doe",
			expiration_date="12/99",
			cvv="123",
			is_default=True,
		)

		response = self.client.get(reverse("get_user", kwargs={"username": self.user.username}))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["credit_cards"][0]["masked_card_number"], "**** **** **** 0366")
		self.assertNotIn("card_number", response.data["credit_cards"][0])
		self.assertNotIn("cvv", response.data["credit_cards"][0])

	def test_update_user_updates_password_and_profile(self):
		response = self.client.patch(
			reverse("update_user", kwargs={"username": self.user.username}),
			{
				"name": "Jonathan Doe",
				"password": "NewPassword789!",
			},
			format="json",
		)

		self.user.refresh_from_db()

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(self.user.name, "Jonathan Doe")
		self.assertTrue(self.user.check_password("NewPassword789!"))
		self.assertNotIn("password", response.data)

	def test_login_user_returns_user_and_credit_cards(self):
		CreditCard.objects.create(
			user=self.user,
			card_number="4532015112830366",
			cardholder_name="John Doe",
			expiration_date="12/99",
			cvv="123",
			is_default=True,
		)

		response = self.client.post(
			reverse("login_user"),
			{
				"username": "johndoe",
				"password": "SecurePassword123!",
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["user"]["username"], "johndoe")
		self.assertEqual(response.data["credit_cards"][0]["masked_card_number"], "**** **** **** 0366")

	def test_create_credit_card_sets_only_one_default(self):
		CreditCard.objects.create(
			user=self.user,
			card_number="4532015112830366",
			cardholder_name="John Doe",
			expiration_date="12/99",
			cvv="123",
			is_default=True,
		)

		response = self.client.post(
			reverse("create_credit_card", kwargs={"username": self.user.username}),
			{
				"card_number": "4485275742308327",
				"cardholder_name": "John Doe",
				"expiration_date": "11/99",
				"cvv": "456",
				"is_default": True,
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(CreditCard.objects.filter(user=self.user, is_default=True).count(), 1)
		self.assertEqual(response.data["masked_card_number"], "**** **** **** 8327")

	def test_create_credit_card_rejects_past_expiration(self):
		response = self.client.post(
			reverse("create_credit_card", kwargs={"username": self.user.username}),
			{
				"card_number": "4485275742308327",
				"cardholder_name": "John Doe",
				"expiration_date": "01/20",
				"cvv": "456",
				"is_default": True,
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("expiration_date", response.data)
