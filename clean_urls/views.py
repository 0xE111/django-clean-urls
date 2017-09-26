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

        last_slug = slug.split('/')[-2]
        for queryset, view in self.settings:
            matches = [instance for instance in queryset.filter(slug=last_slug) if instance.full_slug == slug]
            if len(matches) > 1:
                raise queryset.model.MultipleObjectsReturned('Slug "{slug}" has multiple matches: {matches}'.format(
                    slug=slug,
                    matches='; '.join([str(match) for match in matches]),
                ))
            elif len(matches) == 1:
                return view(*args, **{**kwargs, **{'instance': matches[0]}})

        raise Http404()
