from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category


class SimpleTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse("boardgames:home"))
        self.assertEqual(response.status_code, 200)
    def test_category_creation(self):
        category = Category.objects.create(
            name="Strategy", description="Strategy games"
        )
        self.assertEqual(str(category), "Strategy")
