from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse, resolve

from .models import Info, Stock
from .views import home

client = Client()


class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        """
        Tests status code of response to url
        """
        url = reverse('home')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """
        Tests if url retrieves correct view
        """
        view = resolve('/')
        self.assertEqual(view.func, home)


# class InfoModelTests(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Info

class StockViewTests(TestCase):
    def test_stock_view_status_code(self):
        """
        Tests status code of response to url
        """
        url = reverse('stock')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_stock_url_resolves_home_view(self):
        """
        Tests if url retrieves correct view
        """
        view = resolve('stock/')
        self.assertEqual(view.func, home)