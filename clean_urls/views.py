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


def get_related_field(from_model, to_model):
    # TODO: copy Django's mechanism to search for fk from `from_model` to `to_model` (it definitely has one)
    related_fields = [field for field in from_model._meta.fields if (isinstance(field, (models.ForeignKey, models.OneToOneField)) and field.related_model == to_model)]
    if len(related_fields) != 1:
        raise ImproperlyConfigured('Cannot reslove relation from {from_model} to {to_model}'.format(from_model=from_model, to_model=to_model))

    return related_fields[0].name


class CleanURLHandler():
    def __init__(self, *args):
        """
        Resolves slug paths into corresponding views or raises Http404 exception if resolution fails. Also sets up `get_slug` method for models if possible.

        Args - 2-items tuples: (queryset, view).
        CleanURLHandler subsequently tries to match captured `slug` among querysets' objects, and calls corresponding view on success. The view will also receive matched object as an `instance` kwarg.
        """

        self.settings = args

        # try to define `get_parents` method automatically if possible
        parent_model = None
        for queryset, view in self.settings:
            model = queryset.model

            if not hasattr(model, 'get_parent') and parent_model:  # try to define `get_parent` automatically if undefined
                related_field = get_related_field(model, parent_model)
                model.get_parent = lambda instance: getattr(instance, related_field)  # attrgetter won't work, see http://stackoverflow.com/questions/8906392/python-functions-returned-by-itemgetter-not-working-as-expected-in-classes            

            def get_parents(instance):  # including self
                if isinstance(instance, MpttModel):  # Mptt tree node expands to list of all ancestors and the instance itself
                    expanded = list(instance.get_ancestors(include_self=True))
                elif isinstance(instance, TreebeardModel):  # same for treebeard
                    expanded = list(instance.get_ancestors()) + [instance]
                else:  # single instance is simply converted to a list
                    expanded = [instance]

                parent = expanded[0].get_parent() if hasattr(expanded[0], 'get_parent') else None
                return (parent.get_parents() if parent else []) + expanded

            # TODO: These magic methods are created only when urls.py is imported -> ./manage.py shell won't fire the following code
            model.get_parents = get_parents
            model.get_slug = lambda instance: '/'.join([parent.slug.lower() for parent in instance.get_parents()]) + '/'

            # remember parent model for next iteration
            parent_model = model

    def __call__(self, *args, **kwargs):
        slug = kwargs['slug']
        last_slug = slug.split('/')[-2]

        for queryset, view in self.settings:
            matches = [candidate for candidate in queryset.filter(slug__iexact=last_slug) if candidate.get_slug() == slug]
            if len(matches) == 1:
                kwargs['instance'] = matches[0]
                return view(*args, **kwargs)
            elif len(matches) > 1:
                raise MultipleObjectsReturned('Ambiguous slug [{}], returned {} objects: {}'.format(slug, len(matches), ' / '.join([str(match) for match in matches])))

        raise Http404()
