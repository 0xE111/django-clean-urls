from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class CleanURLHandler:
    def __init__(self, *args):
        """
        Resolves slug paths into corresponding views or raises Http404 exception if resolution fails.

        Args - 2-items tuples: (queryset, view).
        CleanURLHandler subsequently tries to match captured `slug` among querysets' objects, and calls corresponding view on success. The view will also receive matched object as an `instance` kwarg.
        """
        self.settings = args

    def __call__(self, *args, **kwargs):
        slug = kwargs['slug']

        for queryset, view in self.settings:
            try:
                instance = queryset.get(full_slug=slug)
                return view(*args, **{**kwargs, **{'instance': instance}})
            except ObjectDoesNotExist:
                pass

        raise Http404()
