from django import forms

from my_ai.models import ProductDescriptionModel, Language, Tone

language_choices = Language.objects.all().values_list('output_language', 'output_language')
tone_choices = Tone.objects.all().values_list('tone_type', 'tone_type')


class ProductDescriptionForm(forms.ModelForm):
    class Meta:
        model = ProductDescriptionModel
        fields = ['project_name', 'product_name', 'user_description', 'output_language', 'tone']
        widgets = {
            "project_name": forms.TextInput(attrs={"class": "form-control"}),
            "product_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "text",
                    "id": "user_put",
                    "name": "product_name",
                }
            ),
            "user_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "type": "text",
                    "name": "user_description",
                    "cols": "30",
                    "rows": "4",
                    "id": "user_description",
                    'oninput': 'autoHeight(this)',
                }
            ),
            "output_language": forms.Select(
                attrs={"class": 'form-control'}, choices=language_choices
            ),
            "tone": forms.Select(
                attrs={"class": 'form-control'}, choices=tone_choices
            ),

        }
    # editor = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30,'id': 'editor'}))
