from django.core.urlresolvers import reverse
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Photographer(models.Model):
    image = models.ImageField('image')
    slug = models.SlugField()

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('gallery:generic', kwargs={'slug': self.get_slug()})  # CleanURLHandler automatically created 'get_slug' method; for this simple model it will just return self.slug

    def get_categories(self):
        return Category.objects.root_nodes().filter(photographer=self)


class Category(MPTTModel):
    photographer = models.ForeignKey('Photographer')
    parent = TreeForeignKey('self', blank=True, null=True)
    slug = models.CharField('slug', max_length=32)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('gallery:generic', kwargs={'slug': self.get_slug()})

    def get_photos(self):
        return Photo.objects.filter(categories=self)


class Photo(models.Model):
    categories = models.ManyToManyField('Category')
    image = models.ImageField('image')
    slug = models.SlugField()

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('gallery:generic', kwargs={'slug': self.get_slug()})

    def get_parent(self):
        return self.categories.first()  # by default, the first category will be treated as parent
