import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from drivers.models import DriverProfileModel
from users.models import UserProfileModel, UserAddressModel


class TestUsers(TestCase):
    """Unit Test for users app's views"""

    def test_login(self):
        """Test for users login view"""

        user = User.objects.create_user(username='username', password='password')
        url = reverse('users:login')

        # user has no profile not valid
        response = self.client.post(url, {'username': 'username',
                                          'password': 'password'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        DriverProfileModel.objects.create(account=user, phone_number=12345,
                                          profile_photo='/drivers/tests/sample.jpg')

        # user has a driver profile not a user profile
        response = self.client.post(url, {'username': 'username',
                                          'password': 'password'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        UserProfileModel.objects.create(account=user, phone_number=12345)

        # wrong login password
        response = self.client.post(url, {'username': 'username',
                                          'password': 'a wrong password'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # right login
        response = self.client.post(url, {'username': 'username',
                                          'password': 'password'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # user already logged in
        response = self.client.post(url, {'username': 'username',
                                          'password': 'password'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        """Test for users logout view"""

        user = User.objects.create_user(username='username', password='password')

        # user is logged in
        url = reverse('logout')
        self.client.force_login(user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        # user is NOT logged in
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_signup(self):
        """Test for users signup view"""
        url = reverse('users:signup')

        # right sign up
        response = self.client.post(url, {'account': {
            'first_name': 'my first name',
            'last_name': 'my last name',
            'username': 'username',
            'password': 'super_secret'
        },
            'phone_number': 12345},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # already logged in
        response = self.client.post(url, {'account': {
            'username': 'username',
            'password': 'super_secret',
            'first_name': 'my first name',
            'last_name': 'my last name'
        },
            'phone_number': 12345},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        # creating user with a taken username
        self.client.logout()
        response = self.client.post(url, {'account': {
            'username': 'username',  # taken
            'password': 'super_secret',
            'first_name': 'my first name',
            'last_name': 'my last name'
        },
            'phone_number': 12345},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # creating user with a non valid password
        response = self.client.post(url, {'account': {
            'username': 'no_taken_username',
            'password': '123',
            'first_name': 'my first name',
            'last_name': 'my last name'
        },
            'phone_number': 12345},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_user(self):
        """Test for users get view"""

        user = User.objects.create_user(username='username', password='password')
        UserProfileModel.objects.create(account=user, phone_number=12345)
        url = reverse('users:details', kwargs={'username': 'username'})

        # right
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # wrong user
        url = reverse('users:details', kwargs={'username': 'non existing username'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """Test for users update view"""

        user = User.objects.create_user(username='username', password='password')
        UserProfileModel.objects.create(account=user, phone_number=12345)
        url = reverse('users:details', kwargs={'username': 'username'})

        # not logged in as that user
        reponse = self.client.put(url, {'account': {
            'username': 'username',
            'password': 'super_secret',
            'first_name': 'my first name',
            'last_name': 'my last name'
        },
            'phone_number': 12345},
                                  content_type='application/json')
        self.assertEqual(reponse.status_code, 403)

        # not logged in as that user
        user2 = User.objects.create_user(username='username2', password='password')
        UserProfileModel.objects.create(account=user2, phone_number=12345)
        self.client.force_login(user2)
        reponse = self.client.put(url, {'account': {
            'username': 'username',
            'password': 'super_secret',
            'first_name': 'my first name',
            'last_name': 'my last name'
        },
            'phone_number': 12345},
                                  content_type='application/json')
        self.assertEqual(reponse.status_code, 403)

        # wrong or uncomplete data
        self.client.force_login(user)
        reponse = self.client.put(url, {'account': {'first_name': 'my first name'}},
                                  content_type='application/json')
        self.assertEqual(reponse.status_code, 400)

        # uncomplete data passes the patch request right
        reponse = self.client.patch(url, {'account': {'first_name': 'my first name'}},
                                    content_type='application/json')
        self.assertEqual(reponse.status_code, 200)

        # wrong data with patch
        reponse = self.client.patch(url, {'account': {'username': 'username'}},  # duplicate
                                    content_type='application/json')
        self.assertEqual(reponse.status_code, 400)

        # right
        reponse = self.client.put(url, {'account': {
            'username': 'the_new_username',
            'password': 'super_secret',
            'first_name': 'my first name',
            'last_name': 'my last name'
        },
            'phone_number': 12345},
                                  content_type='application/json')
        self.assertEqual(reponse.status_code, 200)

        # wrong username
        url = reverse('users:details', kwargs={'username': 'non existing username'})
        reponse = self.client.put(url, {'account': {
            'username': 'username',
            'password': 'super_secret',
            'first_name': 'my first name',
            'last_name': 'my last name'
        },
            'phone_number': 12345},
                                  content_type='application/json')
        self.assertEqual(reponse.status_code, 404)

    def test_delete_user(self):
        """Test for users delete view"""

        user = User.objects.create_user(username='username', password='password')
        UserProfileModel.objects.create(account=user, phone_number=12345)
        url = reverse('users:details', kwargs={'username': 'username'})

        # is not logged in as that user
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # is not logged in as that user
        user2 = User.objects.create_user(username='username2', password='password')
        UserProfileModel.objects.create(account=user2, phone_number=12345)
        self.client.force_login(user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # wrong username
        self.client.force_login(user)
        url = reverse('users:details', kwargs={'username': 'non existing username'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

        # right
        url = reverse('users:details', kwargs={'username': 'username'})
        self.client.force_login(user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.filter(username='username').exists(), False)


class TestAddresses(TestCase):
    """Unit Test for users addresses views"""

    def test_list_addresses(self):
        """Test for users address list view"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user, phone_number=12345)
        UserAddressModel.objects.create(user=user_profile, title='title', area='area', type='A',
                                        street='street', building='building', location_longitude=0,
                                        location_latitude=0)
        url = reverse('users:addresses-list', kwargs={'username': 'username'})

        # not logged
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # looged in as a user that has no valid user profile
        user2 = User.objects.create_user(username='username2', password='password')
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # not logged in as that user
        user3 = User.objects.create_user(username='username3', password='password')
        UserProfileModel.objects.create(account=user3, phone_number=12345)
        self.client.force_login(user3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # wrong username
        url = reverse('users:addresses-list', kwargs={'username': 'non existing username'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_address(self):
        """Test for users address get view"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user, phone_number=12345)
        UserAddressModel.objects.create(user=user_profile, title='title', area='area', type='A',
                                        street='street', building='building', location_longitude=0,
                                        location_latitude=0)
        url = reverse('users:addresses-detail', kwargs={'username': 'username', 'pk': 1})

        # not logged
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # not logged in as that user
        user2 = User.objects.create_user(username='username2', password='password')
        UserProfileModel.objects.create(account=user2, phone_number=12345)
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # wrong username
        url = reverse('users:addresses-detail', kwargs={'username': 'non existing username',
                                                        'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # wrong address pk
        url = reverse('users:addresses-detail', kwargs={'username': 'username', 'pk': 123})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_address(self):
        """Test for users address create view"""

        user = User.objects.create_user(username='username', password='password')
        UserProfileModel.objects.create(account=user, phone_number=12345)
        url = reverse('users:addresses-list', kwargs={'username': 'username'})

        # not logged
        response = self.client.post(url, {'title': 'title', 'area': 'area', 'type': 'A',
                                          'street': 'street', 'building': 'building',
                                          'location_longitude': 0, 'location_latitude': 0},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # not logged in as that user
        user2 = User.objects.create_user(username='username2', password='password')
        UserProfileModel.objects.create(account=user2, phone_number=12345)
        self.client.force_login(user2)
        response = self.client.post(url, {'title': 'title', 'area': 'area', 'type': 'A',
                                          'street': 'street', 'building': 'building',
                                          'location_longitude': 0, 'location_latitude': 0},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(user)
        response = self.client.post(url, {'title': 'title', 'area': 'area', 'type': 'A',
                                          'street': 'street', 'building': 'building',
                                          'location_longitude': 0, 'location_latitude': 0},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content)['sort'], 1)  # check for sort from signals

        # wrong data
        response = self.client.post(url, {'title': 'title', 'area': 'area', 'type': 'wrong type',
                                          'street': 'street', 'building': 'building'},  # missing attrs
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # wrong username
        url = reverse('users:addresses-list', kwargs={'username': 'non existing username'})
        response = self.client.post(url, {'title': 'title', 'area': 'area', 'type': 'A',
                                          'street': 'street', 'building': 'building',
                                          'location_longitude': 0, 'location_latitude': 0},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_address(self):
        """Test for users address update view"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user, phone_number=12345)
        UserAddressModel.objects.create(user=user_profile, title='title', area='area', type='A',
                                        street='street', building='building', location_longitude=0,
                                        location_latitude=0)
        url = reverse('users:addresses-detail', kwargs={'username': 'username', 'pk': 1})

        # not logged
        response = self.client.put(url, {'title': 'title', 'area': 'area', 'type': 'A',
                                         'street': 'street', 'building': 'building',
                                         'location_longitude': 0, 'location_latitude': 0},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # not logged in as that user
        user2 = User.objects.create_user(username='username2', password='password')
        UserProfileModel.objects.create(account=user2, phone_number=12345)
        self.client.force_login(user2)
        response = self.client.put(url, {'title': 'title', 'area': 'area', 'type': 'A',
                                         'street': 'street', 'building': 'building',
                                         'location_longitude': 0, 'location_latitude': 0},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(user)
        response = self.client.put(url, {'title': 'title', 'area': 'area', 'type': 'A',
                                         'street': 'street', 'building': 'building',
                                         'location_longitude': 0, 'location_latitude': 0},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # wrong data for put
        response = self.client.put(url, {'title': 'title', 'area': 'area', 'type': 'wrong type',
                                         'street': 'street', 'building': 'building'},  # missing attrs
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # right for patch
        response = self.client.patch(url, {'title': 'title', 'area': 'area', 'type': 'A',
                                           'street': 'street', 'building': 'building'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # wrong data
        response = self.client.patch(url, {'title': 'title', 'area': 'area', 'type': 'wrong',
                                           'street': 'street', 'building': 'building'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # wrong username
        url = reverse('users:addresses-detail', kwargs={'username': 'non existing username', 'pk': 1})
        response = self.client.put(url, {'title': 'title', 'area': 'area', 'type': 'A',
                                         'street': 'street', 'building': 'building',
                                         'location_longitude': 0, 'location_latitude': 0},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # wrong address pk
        url = reverse('users:addresses-detail', kwargs={'username': 'username', 'pk': 123})
        response = self.client.put(url, {'title': 'title', 'area': 'area', 'type': 'A',
                                         'street': 'street', 'building': 'building',
                                         'location_longitude': 0, 'location_latitude': 0},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_address(self):
        """Test for users address delete view"""

        user = User.objects.create_user(username='username', password='password')
        user_profile = UserProfileModel.objects.create(account=user, phone_number=12345)
        UserAddressModel.objects.create(user=user_profile, title='title', area='area', type='A',
                                        street='street', building='building', location_longitude=0,
                                        location_latitude=0)
        address2 = UserAddressModel.objects.create(user=user_profile, title='title', area='area', type='A',
                                                   street='street', building='building', location_longitude=0,
                                                   location_latitude=0)
        self.assertEqual(address2.sort, 2)
        url = reverse('users:addresses-detail', kwargs={'username': 'username', 'pk': 1})

        # not logged
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # not logged in as that user
        user2 = User.objects.create_user(username='username2', password='password')
        UserProfileModel.objects.create(account=user2, phone_number=12345)
        self.client.force_login(user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        # right
        self.client.force_login(user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        address2.refresh_from_db()
        self.assertEqual(address2.sort, 1)  # resorted from signals

        # wrong username
        url = reverse('users:addresses-detail', kwargs={'username': 'non existing username', 'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

        # wrong address pk
        url = reverse('users:addresses-detail', kwargs={'username': 'username', 'pk': 123})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
