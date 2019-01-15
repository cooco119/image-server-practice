from django.test import TestCase
from django.urls import reverse
from models.models import Users
import json


# Create your tests here.
class HomeTestCase(TestCase):
    def setUp(self):
        Users.objects.create(name="Alex")
        Users.objects.create(name="jaejun")

    '''
    Testing SignInHandler
    '''
    # Testing basic url configurations
    def test_home_view_sign_in_url_exists_at_desired_location(self):
        response = self.client.get('/home/signin/')
        self.assertEqual(response.status_code, 200)

    def test_home_view_sign_in_accessible_by_name(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)

    # Testing logic
    def test_sign_in_handler_if_sign_in_works(self):
        response = self.client.post(reverse('signin'), {'name': 'Alex'})
        self.assertEqual(response.status_code, 200)

    # def test_sign_in_handler_test_when_value_type_wrong(self):
    #     response = self.client.post(reverse('signin'), {"name":11})
    #     self.assertEqual(response.status_code, 400)
    #
    # => this is handled as the same case when user is not registered

    def test_sign_in_handler_when_key_wrong(self):
        response = self.client.post(reverse('signin'), {"user": "Alex"})
        self.assertEqual(response.status_code, 400)

    def test_sign_in_handler_when_user_not_registered(self):
        response = self.client.post(reverse('signin'), {"name": "Bob"})
        self.assertEqual(response.status_code, 404)

    '''
    Testing GetNoticeHandler
    '''
    # Testing basic url configuration
    def test_home_view_notice_url_exists_at_desired_location(self):
        response = self.client.get('/home/notice/')
        self.assertEqual(response.status_code, 200)

    def test_home_view_notice_accessible_by_name(self):
        response = self.client.get(reverse('notice'))
        self.assertEqual(response.status_code, 200)

    # Testing logic
    def test_get_notice_handler_if_get_works(self):
        response = self.client.get(reverse('notice'))
        self.assertEqual(response.status_code, 200)

    '''
    Testing RegistrationHandler
    '''
    # Testing basic url configuration
    def test_home_view_register_url_exists_at_desired_location(self):
        response = self.client.get('/home/register/')
        self.assertEqual(response.status_code, 200)

    def test_home_view_register_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    # Testing logic
    def test_registration_handler_register_possible(self):
        response = self.client.post(reverse('register'), {"name": "Sam"})
        self.assertEqual(response.status_code, 201)

    def test_registration_handler_when_given_existing_name(self):
        response = self.client.post(reverse('register'), {"name": "Alex"})
        self.assertEqual(response.status_code, 409)