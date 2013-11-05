#-*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User

from dydict.models import Dict
from usermanagement.models import Internaute


class testDict(TestCase):
  def test_create_user(self):
    user = User(username="username",
                password="password",
                email="email@email.fr"
           )
    user.save()
    internaute1 = Internaute(user=user)
    internaute1.save()
    # Check what has been saved
    internaute = Internaute.objects.get(user__username="username")
    self.assertEqual(internaute.user.email, "email@email.fr")

  def test_create_dict(self):
    self.test_create_user()
    internaute = Internaute.objects.get(user__username='username')
    word1 = Dict(word="my_word",
                definition="my definition",
                user_def="my user_def",
                word_ref="my word_ref",
                internaute=internaute)
    word1.save()
    word = Dict.objects.get(word="my_word")
    self.assertEqual(word.word_ref, u'my word_ref')

class SimpleTest(TestCase):
    def test_dydict(self):
        """
        check dydict views
        """
        self.assertEqual(1 + 1, 2)
