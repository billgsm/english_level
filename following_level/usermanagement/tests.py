from django.test import TestCase, Client
from django.contrib.auth.models import User


class StatusTest(TestCase):
  def setUp(self):
    self.client = Client()

  def test_public(self):
    urls = ({'url': '/user/login/',
             'template': 'user/login.html',
             'status': 200},
            {'url': '/user/logout/',
             'template': 'user/login.html',
             'status': 302},
            {'url': '/user/profile/',
             'template': 'user/login.html',
             'status': 302},
           )
    for url in urls:
      response = self.client.get(url['url'])
      self.assertEqual(response.status_code, url['status'])
      response = self.client.get(url['url'], follow=True)
      self.assertEqual(response.template_name, url['template'])

  def test_register_form(self):
    form = {
            'username': 'john',
            'password1': 'ggggggg',
            'password2': 'ggggggg',
           }
    response = self.client.post('/user/create_account/', form, follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name[0], 'user/success.html')
    user = User.objects.get(username='john')
    self.assertEqual(user.username, 'john')

  def test_register_form_fail(self):
    form = {
            'username': 'john',
            'password1': 'ggggggg',
            'password2': 'ggg',
           }
    response = self.client.post('/user/create_account/', form, follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'user/create.html')

  def test_login(self):
    self.test_register_form()
    form = {
            'username': 'john',
            'password': 'ggggggg',
           }
    response = self.client.post('/user/login/', form, follow=True)
    self.assertEqual(response.templates[0].name, 'user/profile.html')

  def test_login_fail(self):
    self.test_register_form()
    form = {
            'username': 'john',
            'password': 'gg',
           }
    response = self.client.post('/user/login/', form, follow=True)
    self.assertEqual(response.template_name, 'user/login.html')


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
