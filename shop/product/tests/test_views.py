from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from product.models import Category, Product


class ViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='MikeyMouse', email='test@mail.com')
        cls.category = Category.objects.create(
            name='Тестовая группа',
            slug='test_slug',
        )
        cls.product = Product.objects.create(
            name='Тестовый товар',
            price=12,
            slug='test_slug'
        )

    def setUp(self):
        self.guest_client = Client()
        self.customer_client = Client()
        self.customer_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'product/index.html': reverse('index'),
            'product/product_detail.html': (
                reverse('product_detail', kwargs={'product_slug': self.product.slug})
            ),

        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

