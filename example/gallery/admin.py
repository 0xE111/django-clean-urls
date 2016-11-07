from django.contrib import admin

from .models import Photographer, Category


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
