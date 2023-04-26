from django.test import TestCase

from accounts.models import CustomUser
from .models import ProductDescriptionModel, Templates, Tone, Language


class ProductDescriptionModelTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            password='testpass',
            email='testemail@gmail.com'
        )
        self.template = Templates.objects.create(name='Test Template')
        self.tone = Tone.objects.create(tone_type='Test Tone')
        self.language = Language.objects.create(output_language='Test Language')
        self.product = ProductDescriptionModel.objects.create(
            template_name=self.template,
            tone=self.tone,
            output_language=self.language,
            project_name='Test Project',
            product_name='Test Product',
            user_description='Test Description',
            client=self.user
        )

    def test_product_description_model(self):
        product = self.product
        self.assertEqual(product.template_name, self.template)
        self.assertEqual(product.tone, self.tone)
        self.assertEqual(product.output_language, self.language)
        self.assertEqual(product.project_name, 'Test Project')
        self.assertEqual(product.product_name, 'Test Product')
        self.assertEqual(product.user_description, 'Test Description')
        self.assertEqual(product.client, self.user)


class TemplateModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Templates.objects.create(name='Test Template', temperature=0.8, model='text-davinci-002')

    def test_name_label(self):
        template = Templates.objects.get(name='Test Template')
        field_label = template._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'template name')

    def test_description_label(self):
        template = Templates.objects.get(name='Test Template')
        field_label = template._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'template description')

    def test_template_max_token(self):
        template = Templates.objects.get(name='Test Template')
        max_token = template.max_token
        self.assertEquals(max_token, 255)

    def test_template_model(self):
        template = Templates.objects.get(name='Test Template')
        model = template.model
        self.assertEquals(model, 'text-davinci-002')

    def test_template_temperature(self):
        template = Templates.objects.get(name='Test Template')
        temperature = template.temperature
        self.assertEquals(float(temperature), 0.8)

    def test_is_published(self):
        template = Templates.objects.get(name='Test Template')
        is_published = template.is_published
        self.assertFalse(is_published)  # By default, is_published should be False

    def test_is_product_name_required(self):
        template = Templates.objects.get(name='Test Template')
        is_product_name_required = template.is_product_name_required
        self.assertTrue(is_product_name_required)  # By default, is_product_name_required should be True
