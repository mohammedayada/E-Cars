from django.contrib import admin
from .models import Car
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = []
    list_display_links = []
    list_filter = []
    search_fields = []

admin.site.register(Car)
