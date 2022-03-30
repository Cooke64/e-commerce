from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from product.models import Category, Product


class ViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            name='Тестовый заголовок',
            slug='test-slug',
        )
        cls.product = Product.objects.create(
            name='Тестовый продукт',
            slug='test_slug',
            price=123.00,
            category=cls.category
        )

    def setUp(self):
        self.user = User.objects.create_user(username='Тестер')
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

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

