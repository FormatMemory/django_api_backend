from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from core.models import User
from user.serializers import UserSerializer


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")
DELETE_TOKEN_URL = reverse("user:delete_token")
USER_LIST_URL = reverse("user:user_list")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test the users API (public)
    """
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful
        """
        payload = {
            "email": "test@tt.com",
            "password": "testpass",
            "name": "TestName"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """
        Test creating a user that already exists fails
        """
        payload = {
            "email": "test@tt.com",
            "password": "testpass",
            "name": "TestName"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that password must be more than 5 characters
        """
        payload = {
            "email": "test@tt.com",
            "password": "ps",
            "name": "TestName"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # user not created
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Test that a token is created for the user
        """
        payload = {
            "email": "test@test.com",
            "password": "testpassword"
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        Test that token is not created if invalid credentials are given
        """
        payload = {
            "email": "test@test.com",
            "password": "testpassword"
        }
        create_user(**payload)
        payload["password"] = "wrongPassWord"
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        Test that token is not created if user doesn't exist
        """
        payload = {
            "email": "test@test.com",
            "password": "testpassword"
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # user not created
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_missing_field(self):
        """
        Test that email and password are required
        """
        res = self.client.post(TOKEN_URL, {
            "email": "test@test.com",
            "password": ""
            })
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        """
        Test that authentication is required for users
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_not_able_to_delete_token(self):
        """
        Test that authentication is required for delete token
        """
        res = self.client.get(DELETE_TOKEN_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_not_able_to_view_user_list(self):
        """
        Test that authentication is required for view user list
        """
        res = self.client.get(USER_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        test_cases = [
            {"xx": "12"},
            {"email": "test@test.com"},
            {"email": "dqw"},
            {"pk": "1"},
            {"name": "qwe"}
        ]
        for tc in test_cases:
            res = self.client.get(USER_LIST_URL, tc)
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """
    Test API requests that require authentication
    """

    def setUp(self):
        self.user = create_user(
            email="test@test.com",
            password="testpassword",
            name="TestName"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        """
        Test retriving profile for logged in users
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "name": self.user.name,
            "email": self.user.email
        })

    def test_post_me_not_allowed(self):
        """
        Test that POST is not allowed on the me url
        """
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test updating the user profile for authenticated user
        """
        payload = {
            "name": "New Name",
            "password": "newPassword123@"
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_email_cannot_change(self):
        """
        Test updating the user profile for authenticated user
        while email cannot be changed
        """
        payload = {
            "name": "New Name",
            "password": "newPassword123@",
            "email": "22@test.com"
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "name": payload["name"],
            "email": self.user.email
        })
        self.assertTrue(self.user.check_password(payload["password"]))

    def test_user_delete_token_success(self):
        """
        Test authenticated user logout to make old token invalid
        """
        old_token = Token.objects.get_or_create(user=self.user)
        res = self.client.get(DELETE_TOKEN_URL)
        new_token = Token.objects.get_or_create(user=self.user)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(old_token, new_token)

    def test_normal_user_cannot_access_user_list(self):
        """
        Test normal authenticated user cannot access userlist
        """
        res = self.client.get(USER_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        test_cases = [
            {"xx": "12"},
            {"email": "test@test.com"},
            {"email": "dqw"},
            {"pk": "1"},
            {"name": "qwe"}
        ]
        for tc in test_cases:
            res = self.client.get(USER_LIST_URL, tc)
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserAPITest(TestCase):
    """
    Test API requests that require admin permission
    """

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="testpassword",
            name="TestName"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_list_respond_correct_data(self):
        """
        Test admin user access user_list returns correct data
        """
        user1_payload = {
            "email": "test1@test.com",
            "password": "qiwdojioqw21e",
            "name": "user1name"
        }
        user2_payload = {
            "email": "test2@test.com",
            "password": "adnojioqw21e",
            "name": "user2name"
        }
        create_user(**user1_payload)
        create_user(**user2_payload)

        res = self.client.get(USER_LIST_URL)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        test_cases = {
           ("xx", "12"): 0,
           ("email", "test@test.com"): 1,
           ("email", "dqw"): 0,
           ("name", "qwe"): 0,
           ("name", "user1name"): 1
        }
        for test_arg, exp_res in test_cases.items():
            res = self.client.get(USER_LIST_URL, {test_arg[0]: test_arg[1]})
            # print(test_arg, len(res.data), exp_res, res.data)
            self.assertEqual(len(res.data), exp_res)
