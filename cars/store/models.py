from django.dispatch import receiver
from .slugify import unique_slug_generator
from django.db import models
from django.conf import settings
from django.shortcuts import reverse

from colorfield.fields import ColorField
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator



def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


CATEGORY_CHOICES = (
    ('M', 'mercedes'),
    ('A', 'Audi'),
    ('B', 'BMW')
)
LABEL_CHOICES = (
    ('S', 'Sold'),
    ('F', 'For sale'),
    ('O', 'Offer')
)
GEAR_CHOICES = (
    ('M', 'Manuel'),
    ('A', 'Automatic'),
    ('S', 'Steptronic'),
    ('E', 'Easy Tronic')
)
STATE_CHOICES = (
    ('U', 'Used'),
    ('N', 'new'),
)
CAPACITY_CHOICES = (
    ('A', 'Less than 1000cc'),
    ('B', 'From 1000cc to 1300cc'),
    ('C', 'More than 1300cc to 1500cc'),
    ('D', 'More than 1500cc to 2000cc'),
    ('E', 'more than 2000cc')
)

STRUCTURE_CHOICES = (
    ('A', 'Hatchback'),
    ('B', 'Sedan'),
    ('C', 'MUV/SUV'),
    ('D', 'Coupe'),
    ('E', 'Convertible'),
    ('F', 'Wagon'),
    ('J', 'Van'),
    ('K', 'Jeep'),
)
AD_TYPE_CHOICES = (
    ('A', 'Exchange with highest'),
    ('B', 'Exchange with less'),
    ('F', 'For sale'),
    ('I', 'Installment sales')
)

class Car(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    model = models.CharField(max_length=20)
    manufacturing_year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1950), max_value_current_year])
    capacity = models.CharField(choices=CAPACITY_CHOICES, max_length=2)
    gearbox = models.CharField(choices=GEAR_CHOICES, max_length=2)  # gear box
    structure = models.CharField(choices=STRUCTURE_CHOICES, max_length=2)
    Kilometers = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2) #car type
    color = ColorField()
    Ad_type = models.CharField(choices=AD_TYPE_CHOICES, max_length=2)
    description = models.TextField()
    image = models.ImageField()
    Publish_date = models.DateTimeField(auto_now_add=True)
    telephone = models.CharField(max_length=11, blank=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2)
    slug = models.SlugField(unique=True, null=True, blank=True)


    def __str__(self):
        return f'{self.model} of {self.title }'
    def get_absolute_url(self):
        return reverse('store:product', kwargs={
            'slug': self.slug
        })

@receiver(models.signals.pre_save, sender=Car)
def auto_slug_generator(sender, instance, **kwargs):
    """Creates a slug if there is no slug. """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

