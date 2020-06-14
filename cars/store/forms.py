from django.forms import Form, ChoiceField, CharField
from django import forms
from .models import Car, CAPACITY_CHOICES, CATEGORY_CHOICES,GEAR_CHOICES, STRUCTURE_CHOICES, STATE_CHOICES, AD_TYPE_CHOICES, LABEL_CHOICES
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'title',
            'image',
            'price',
            'model',
            'manufacturing_year',
            'capacity',
            'gearbox',
            'structure',
            'Kilometers',
            'state',
            'category',
            'color',
            'Ad_type',
            'description',
            'label',
            'telephone'
        ]

class FilterForm(Form):

    category_field = ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select'
    }))