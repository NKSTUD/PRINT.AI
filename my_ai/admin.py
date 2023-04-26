from django.contrib import admin

from my_ai.models import ProductDescriptionModel, Templates, AiDescription, Tone, Language, TemplateCategory


class ProductAdminModel(admin.ModelAdmin):
    list_display = ('product_name', 'project_name', 'template_name',)


class TemplatesAdminModel(admin.ModelAdmin):
    list_display = ("name", 'category','is_published', 'is_product_name_required', 'usage_rate')
    list_editable = ('category', 'is_published', 'is_product_name_required')
    list_filter = ('category',)


class TemplateCategoryAdminModel(admin.ModelAdmin):
    list_display = ("name", "get_templates")


class AiDescriptionAdminModel(admin.ModelAdmin):
    list_display = ('ai_product_name', "ai_answer", "client",)


class ToneAdminModel(admin.ModelAdmin):
    list_display = ('tone_type',)


class LanguageAdminModel(admin.ModelAdmin):
    list_display = ('output_language',)


admin.site.register(AiDescription, AiDescriptionAdminModel)
admin.site.register(ProductDescriptionModel, ProductAdminModel)
admin.site.register(Templates, TemplatesAdminModel)
admin.site.register(Tone, ToneAdminModel)
admin.site.register(Language, LanguageAdminModel)
admin.site.register(TemplateCategory, TemplateCategoryAdminModel)
