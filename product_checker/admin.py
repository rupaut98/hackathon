from django.contrib import admin
from .models import Ingredient

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_unhealthy', 'description', 'country_banned_in', 'severity')  # Add 'description' to list_display
    search_fields = ('name', 'description', 'country_banned_in', 'severity')  # Add 'description' to search_fields

admin.site.register(Ingredient, IngredientAdmin)
