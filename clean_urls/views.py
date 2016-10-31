from operator import attrgetter

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.http import Http404


class CleanURLHandler():
    def __init__(self, *args):
        """
        Resolves slug paths into corresponding views or raises Http404 exception if resolution fails. Also sets up `get_slug` method for models if possible.

        Args - 2-items tuples: (queryset, view).
        CleanURLHandler subsequently tries to match captured `slug` among querysets' objects, and calls corresponding view on success. The view will also receive matched object as an `instance` kwarg.
        """

        self.settings = *args

        # try to define `get_slug` method automatically if possible
        parent_model = None
        for i, (queryset, view) in enumerate(self.settings):
            model = queryset.model

            if hasattr(model, 'get_slug'):  # if user already defined `get_slug` method, leave it as is
                continue

            # define how to get slug for instance depending on its class
            if isinstance(instance, MPTTModel):
                get_instance_slug = lambda instance: '/'.join(instance.get_ancestors(include_self=True).values_list('slug', flat=True))
            # elif isinstance(instance, TreeBeard):  # ?????????????//
            #     pass
            else:
                get_instance_slug = attrgetter('slug')

            # define how to get parent model's slug
            if not parent_model:
                parent_field = None
            else:
                for field in model._meta.fields:
                    if isinstance(field, (models.ForeignKey, models.OneToOneField)) and field.related_model == parent_model:
                        # TODO: only first match is captured!!!!!!!!!!!!!
                        parent_field = field.name
                        break
                else:
                    raise ImproperlyConfigured('Cannot reslove relation from {child_model} to {parent_model}, please define `get_slug` method on {child_model} explicitly'.format(child_model=model, parent_model=parent_model))

            
            get_parent_slug = lambda instance: getattr(instance, parent_field).get_slug() if parent_field else ''

            # define get_slug == parent model's slug + instance's slug
            model.get_slug = get_parent_slug(instance) + get_instance_slug(instance)

            # remember parent model for next iteration
            parent_model = model

    def __call__(self, request, slug, *args, **kwargs):
        last_slug = slug.split('/')[-2]

        for queryset, view in self.settings:
            matches = [candidate for candidate in self.queryset.filter(slug=last_slug) if candidate.get_slug() == slug]
            if len(matches) == 1:
                return view(request, instance=matches[0], *args, **kwargs)
            elif len(matches) > 1:
                raise MultipleObjectsReturned('Ambiguous slug [{}], returned {} objects: {}'.format(slug, len(matches), ' / '.join([str(match) for match in matches])))

        raise Http404()
