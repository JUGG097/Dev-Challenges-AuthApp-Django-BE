from rest_framework.test import APITestCase
from django.urls import reverse


# Create your tests here.
class AuthAppTests(APITestCase):
    def successful_signup(self):
        url = reverse("user_signup")
        response = self.client.post(
            url,
            data={
                "email": "foo@bar.com",
                "password": "zxcvbn123456",
                "provider": "LOCAL",
            },
            format="json",
        )

        return response

    def successful_signup_login(self):
        response = self.successful_signup()
        assert response.status_code == 200

        url = reverse("user_login")
        response2 = self.client.post(
            url,
            data={
                "email": "foo@bar.com",
                "password": "zxcvbn123456",
                "provider": "LOCAL",
            },
            format="json",
        )

        return response2

    def test_sign_up_happyflow(self):
        """
        Tests Sign Up Happy Flow
        """
        response = self.successful_signup()
        resp_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data["success"], True)
        self.assertEqual(resp_data["data"]["email"], "foo@bar.com")

    def test_sign_up_unhappyflow(self):
        """
        Tests Sign Up Unhappy Flow
        """
        url = reverse("user_signup")
        response = self.client.post(
            url,
            data={
                "email": "foo@bar.com",
                "password": "zxcvbn123456",
                "providerssss": "LOCAL",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_log_in_happyflow(self):
        """
        Tests Login Happy Flow
        """
        response = self.successful_signup()
        self.assertEqual(response.status_code, 200)

        url = reverse("user_login")
        response2 = self.client.post(
            url,
            data={
                "email": "foo@bar.com",
                "password": "zxcvbn123456",
                "provider": "LOCAL",
            },
            format="json",
        )
        resp_data = response2.json()
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(resp_data["success"], True)
        self.assertEqual(resp_data["data"]["email"], "foo@bar.com")

    def test_log_in_unhappyflow(self):
        """
        Tests Login Unhappy Flow
        """
        response = self.successful_signup()
        self.assertEqual(response.status_code, 200)

        url = reverse("user_login")
        response2 = self.client.post(
            url,
            data={
                "email": "foo@bar.com",
                "password": "qwerty123456",
                "provider": "LOCAL",
            },
            format="json",
        )
        self.assertEqual(response2.status_code, 400)

    def test_refreshToken_happyflow(self):
        """
        Tests Refresh Token Happy Flow
        """
        response = self.successful_signup_login()
        self.assertEqual(response.status_code, 200)

        url = reverse("refresh_token")
        response2 = self.client.post(
            url,
            data={
                "refreshToken": response.json()["refreshToken"],
            },
            format="json",
        )
        resp_data = response2.json()
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(resp_data["success"], True)
        self.assertEqual(resp_data["refreshToken"], response.json()["refreshToken"])

    def test_refreshToken_unhappyflow(self):
        """
        Tests Refresh Token Unhappy Flow
        """
        response = self.successful_signup_login()
        self.assertEqual(response.status_code, 200)

        url = reverse("refresh_token")
        response2 = self.client.post(
            url,
            data={
                "refreshToken": "",
            },
            format="json",
        )
        resp_data = response2.json()
        self.assertEqual(response2.status_code, 401)
        self.assertEqual(resp_data["success"], False)

    def test_fetch_profile_happyflow(self):
        """
        Tests Fetching User Profile Happy Flow
        """
        response = self.successful_signup_login()
        self.assertEqual(response.status_code, 200)

        # Added token to request header
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.json()["authToken"]
        )
        url = reverse("user_profile")
        response2 = self.client.get(url, format="json")
        resp_data = response2.json()
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(resp_data["success"], True)
        self.assertEqual(resp_data["data"]["email"], "foo@bar.com")

    def test_fetch_profile_unhappyflow(self):
        """
        Tests Fetching User Profile Unhappy Flow
        """
        response = self.successful_signup_login()
        self.assertEqual(response.status_code, 200)

        url = reverse("user_profile")
        response2 = self.client.get(
            url,
        )
        self.assertEqual(response2.status_code, 401)

    def test_update_profile_happyflow(self):
        """
        Tests Updating User Profile Happy Flow
        """
        response = self.successful_signup_login()
        self.assertEqual(response.status_code, 200)

        # Added token to request header
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.json()["authToken"]
        )
        url = reverse("edit_user_profile")
        response2 = self.client.put(url, data={"name": "John Doe"}, format="json")
        resp_data = response2.json()
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(resp_data["success"], True)
        self.assertEqual(resp_data["data"]["name"], "John Doe")

    def test_update_profile_unhappyflow(self):
        """
        Tests Updating User Profile Unhappy Flow
        """
        response = self.successful_signup_login()
        self.assertEqual(response.status_code, 200)

        url = reverse("edit_user_profile")
        response2 = self.client.get(
            url,
        )
        self.assertEqual(response2.status_code, 401)
