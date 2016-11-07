from django.contrib import admin

from .models import Photographer, Category, Photo


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
