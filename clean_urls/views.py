from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.http import Http404

try:
    from mptt.models import MPTTModel as MpttModel
except ImportError:
    MpttModel = None

try:
    from treebeard.models import Node as TreebeardModel
except ImportError:
    TreebeardModel = None


class CleanURLHandler():
    def __init__(self, *args):
        """
        Resolves slug paths into corresponding views or raises Http404 exception if resolution fails. Also sets up `get_slug` method for models if possible.

        Args - 2-items tuples: (queryset, view).
        CleanURLHandler subsequently tries to match captured `slug` among querysets' objects, and calls corresponding view on success. The view will also receive matched object as an `instance` kwarg.
        """

        self.settings = args

        # try to define `get_slug` method automatically if possible
        parent_model = None
        for queryset, view in self.settings:
            model = queryset.model

            if hasattr(model, 'get_slug'):  # if user already defined `get_slug` method, leave it as is
                continue

            # define how to get slug for model depending on its class
            if issubclass(model, MpttModel):
                get_instance_slug = lambda instance: '/'.join(instance.get_ancestors(include_self=True).values_list('slug', flat=True)) + '/'
            elif issubclass(model, TreebeardModel):
                get_instance_slug = lambda instance: '/'.join([ancestor.slug for ancestor in (list(instance.get_ancestors()) + [instance])]) + '/'
            else:
                get_instance_slug = lambda instance: instance.slug + '/'

            # define how to get parent model's slug
            get_parent_slug = lambda instance: ''  # default

            if parent_model:
                related_fields = [field for field in model._meta.fields if (isinstance(field, (models.ForeignKey, models.OneToOneField)) and field.related_model == parent_model)]
                if len(related_fields) == 1:
                    parent_field = related_fields[0].name
                    get_parent_slug = lambda instance: getattr(instance, parent_field).get_slug()
                else:
                    raise ImproperlyConfigured('Cannot reslove relation from {child_model} to {parent_model}, please define `get_slug` method on {child_model} explicitly'.format(child_model=model, parent_model=parent_model))                    

            # define get_slug == parent model's slug + instance's slug
            model.get_slug = lambda instance: get_parent_slug(instance) + get_instance_slug(instance)

            # remember parent model for next iteration
            parent_model = model

    def __call__(self, *args, **kwargs):
        slug = kwargs['slug']
        last_slug = slug.split('/')[-2]

        for queryset, view in self.settings:
            matches = [candidate for candidate in queryset.filter(slug=last_slug) if candidate.get_slug() == slug]
            if len(matches) == 1:
                kwargs['instance'] = matches[0]
                return view(*args, **kwargs)
            elif len(matches) > 1:
                raise MultipleObjectsReturned('Ambiguous slug [{}], returned {} objects: {}'.format(slug, len(matches), ' / '.join([str(match) for match in matches])))

        raise Http404()
