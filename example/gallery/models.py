from django.core.urlresolvers import reverse
from django.db import models


class Photographer(models.Model):
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('gallery:generic', kwargs={'slug': self.get_slug()})  # CleanURLHandler automatically created 'get_slug' method; for this simple model it will just return self.slug