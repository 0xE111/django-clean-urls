from django.db import models


class CleanURLMixin(models.Model):
    class Meta:
        abstract = True

    def get_parent(self):
        raise NotImplementedError('You must define "get_parent" method for {}'.format(self.__class__.__name__))

    def get_parents(self):  # includes self
        parent = self.get_parent()
        return (list(parent.get_parents()) if parent else []) + [self]

    # TODO: cache this
    @property
    def full_slug(self, *args, **kwargs):
        return '/'.join([parent.slug for parent in self.get_parents()]) + '/'
