from django.conf import settings
from django.db import models
from django.db.models import TextField
from django.utils.translation import gettext_lazy as _

from default_prompts import ProductDescription_prompt

User = settings.AUTH_USER_MODEL


class TemplateCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name=_("template category"))

    class Meta:
        verbose_name_plural = _("Template Categories")

    def __str__(self):
        return self.name

    def get_template_names(self):
        return [template.name for template in Templates.objects.filter(category=self)]

    def get_templates(self):
        return list(Templates.objects.filter(category=self))


"""I.CREATE TEMPLATES MODELS  """


class Templates(models.Model):
    name = models.CharField(max_length=225, blank=False, unique=True,
                            verbose_name="template name")
    category = models.ForeignKey(to=TemplateCategory, blank=True, null=True, verbose_name='template category',
                                 on_delete=models.SET_NULL)
    description = TextField(blank=True, verbose_name=_('template description'))
    prompt = models.TextField(blank=True, null=False, default=_(ProductDescription_prompt),
                              verbose_name=_("template prompt"))
    max_token = models.PositiveIntegerField(verbose_name="max token", null=False, blank=True, default=255)
    temperature = models.FloatField(default=0.7)
    frequency_penalty = models.FloatField(default=0.0)
    model = models.CharField(max_length=100, blank=True, default="text-davinci-003")
    product_name_label = models.CharField(max_length=150, blank=True, null=False, default=_('Your Product Name Here'))
    product_name_placeholder = models.CharField(max_length=125, blank=True, null=False,
                                                default=_('Print.ai'))
    user_description_label = models.CharField(max_length=300, blank=True, null=False,
                                              default=_('Provide Some description for your product :'))
    user_description_placeholder = models.TextField(blank=True, null=False,
                                                    default=_('Best AI copy writing app to make it easier !'), )
    is_published = models.BooleanField(default=False)
    is_product_name_required = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Templates")

    def __str__(self):
        return self.name

    # Get or create a default template, if template doesn't exist create it else get it
    @classmethod
    def get_default_template(cls):
        default_template, _ = cls.objects.get_or_create(name="Product Descriptions")
        return default_template

    def usage_rate(self):
        return f'{round((self.productdescriptionmodel_set.count() / ProductDescriptionModel.objects.count()) * 100, 2)}%'


class Language(models.Model):
    output_language = models.CharField(max_length=225, blank=False, unique=True,
                                       verbose_name=_("output language"))

    def __str__(self):
        return self.output_language

    @classmethod
    def get_default_language(cls):
        default_language, _ = cls.objects.get_or_create(output_language="English (American English) en")
        return default_language


class Tone(models.Model):
    tone_type = models.CharField(max_length=225, blank=False, unique=True,
                                 verbose_name=_("Tone"))

    def __str__(self):
        return self.tone_type

    @classmethod
    def get_default_tone(cls):
        default_tone, _ = cls.objects.get_or_create(tone_type="Friendly")
        return default_tone


"""CREATE PRODUCT DESCRIPTION MODEL"""


class ProductDescriptionModel(models.Model):
    template_name = models.ForeignKey(to=Templates,
                                      on_delete=models.SET_DEFAULT,
                                      blank=False, to_field="name",
                                      default=Templates.get_default_template,
                                      verbose_name=_('template name'))
    tone = models.ForeignKey(to=Tone,
                             on_delete=models.SET_DEFAULT,
                             blank=False, to_field="tone_type",
                             default=Tone.get_default_tone,
                             verbose_name='tone_type')
    output_language = models.ForeignKey(to=Language,
                                        on_delete=models.SET_DEFAULT,
                                        blank=False, to_field="output_language",
                                        default=Language.get_default_language,
                                        verbose_name=_('output language'))
    project_name = models.CharField(max_length=250, blank=True, verbose_name=_('Project Name'), )
    product_name = models.CharField(max_length=250, null=False, blank=True, verbose_name=_('Product Name'))
    user_description = models.TextField(max_length=1000, blank=True, verbose_name=_("user description"))
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.project_name

    def product_ai_description(self):
        return self.aidescription_set.all()


class AiDescription(models.Model):
    ai_product_name = models.ForeignKey(to=ProductDescriptionModel,
                                        on_delete=models.CASCADE, blank=True, null=True, verbose_name="ai_product")
    ai_answer = models.TextField(blank=True, verbose_name='ai_product_description', null=True)
    template_name = models.CharField(blank=True, null=True, max_length=150)

    class Meta:
        ordering = ['-id']

    def client(self):
        return self.ai_product_name.client

    def __str__(self):
        return str(self.ai_product_name)
