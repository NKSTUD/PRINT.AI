from django import forms
from my_ai.models import ProductDescriptionModel, Language, Tone


def get_language_choices():
    return Language.objects.all().values_list('output_language', 'output_language')


def get_tone_choices():
    return Tone.objects.all().values_list('tone_type', 'tone_type')


class ProductDescriptionForm(forms.ModelForm):
    output_language = forms.ModelChoiceField(queryset=Language.objects.all(), empty_label=None,
                                             widget=forms.Select(attrs={"class": 'form-control'}))
    tone = forms.ModelChoiceField(queryset=Tone.objects.all(),
                                  widget=forms.Select(attrs={"class": 'form-control'}),
                                  empty_label=None)

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
            )
        }
