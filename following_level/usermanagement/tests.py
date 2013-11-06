from django.test import TestCase, Client
from django.contrib.auth.models import User

from usermanagement.models import Internaute


class StatusTest(TestCase):
  def setUp(self):
    self.client = Client()

  def test_public(self):
    urls = ({'url': '/user/login/',
             'template': 'usermanagement/login.html',
             'status': 200},
            {'url': '/user/logout/',
             'template': 'usermanagement/login.html',
             'status': 302},
            {'url': '/dictionary/list/',
             'template': 'usermanagement/login.html',
             'status': 302},
            {'url': '/user/createuser/',
             'template': 'usermanagement/register.html',
             'status': 200},
           )
    for url in urls:
      response = self.client.get(url['url'])
      self.assertEqual(response.status_code, url['status'])
      response = self.client.get(url['url'], follow=True)
      self.assertEqual(response.templates[0].name, url['template'])

  def test_register_form(self):
    form = {
            'username': 'john',
            'password': 'ggggggg',
            're_password': 'ggggggg',
            'email': 'john@john.com',
           }
    response = self.client.post('/user/createuser/', form, follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'dydict/dict_list.html')
    user = Internaute.objects.get(user__username='john')
    self.assertEqual(user.user.username, 'john')

  def test_register_form_fail(self):
    form = {
            'username': 'john',
            'password1': 'ggggggg',
            'password2': 'ggg',
            'email': 'john@john.com',
           }
    response = self.client.post('/user/createuser/',
                                form,
                                follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'usermanagement/register.html')

  def test_login(self):
    self.test_register_form()
    response = self.client.get('/user/logout/')
    form = {
            'username': 'john',
            'password': 'ggggggg',
           }
    response = self.client.post('/user/login/', form, follow=True)
    self.assertEqual(response.templates[0].name, 'dydict/dict_list.html')

  def test_login_fail(self):
    self.test_register_form()
    response = self.client.get('/user/logout/')
    form = {
            'username': 'john',
            'password': '00',
           }
    response = self.client.post('/user/login/', form, follow=True)
    self.assertEqual(response.templates[0].name, 'usermanagement/login.html')
