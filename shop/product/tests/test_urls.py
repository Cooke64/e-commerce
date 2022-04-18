from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from product.models import Category, Store, Product

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='MikeyMouse', email='test@mail.com')
        cls.category = Category.objects.create(
            name='Тестовая группа',
            slug='test_slug',
        )
        cls.store = Store.objects.create(
            name='Тестовый магазин',
        )
        cls.product = Product.objects.create(
            name='Тестовый товар',
            price=12,
            slug='test_slug'
        )
        cls.pages_list = [
            '/',
            '/category/test_slug/',
            '/product/test_slug/',
        ]

    def setUp(self):
        self.guest_client = Client()
        self.customer_client = Client()
        self.customer_client.force_login(self.user)

    def test_public_pages(self):
        """Проверяем вход незарегистрированного пользователя
        на общедоступные страницы.
        """
        for page in self.pages_list[:4]:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, 200)