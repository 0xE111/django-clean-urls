from django.db import models


class CleanURLMixin(models.Model):
    MAX_LENGTH = 255

    full_slug = models.CharField(editable=False, max_length=MAX_LENGTH, unique=True)

    class Meta:
        abstract = True

    def get_parent(self):
        raise NotImplementedError('You must define "get_parent" method for {}'.format(self.__class__.__name__))

    def get_parents(self):  # includes self
        parent = self.get_parent()
        return (parent.get_parents() if parent else []) + [self]

    def get_full_slug(self, *args, **kwargs):
        return '/'.join([parent.slug for parent in self.get_parents()])[:self.MAX_LENGTH-1] + '/'

    def save(self, *args, **kwargs):
        if not self.full_slug:
            self.full_slug = self.get_full_slug()
        return super().save(*args, **kwargs)

