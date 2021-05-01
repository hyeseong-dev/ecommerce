from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class TestBasketView(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
        Category.objects.create(name='book', slug='book')
        Product.objects.create(category_id=1, title='delicious kimchi', created_by_id=1,
                               slug='delicious-kimchi', price='200.00', image='kimchi')
        Product.objects.create(category_id=1, title='spicy kimch', created_by_id=1,
                               slug='delicious-kimchi', price='200.00', image='kimchi')
        Product.objects.create(category_id=1, title='sweet kimchi', created_by_id=1,
                               slug='delicious-kimchi', price='200.00', image='kimchi')
        self.client.post(
            reverse('basket:basket_add'), {"productid": 1, "productqty": 1, "action": "post"}, xhr=True)
        self.client.post(
            reverse('basket:basket_add'), {"productid": 2, "productqty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket
        """
        response = self.client.post(
            reverse('basket:basket_add'), {"productid": 3, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('basket:basket_add'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_delete'), {"productid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '200.00'})

    def test_basket_update(self):
        """
        Test updating items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_update'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '400.00'})
