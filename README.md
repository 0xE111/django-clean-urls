# django-clean-urls
Package for creation hierarchical clean URLs in Django.

## Overview
Django by default forces developers to use *static* URLs - by the word "static" I mean both fixed URL depth and that each URL is constant except some small chunks that change (usually instance's `pk` and/or `slug`). This works fine 'till you get some hierarchy of unpredictable depth in your models.

Consider an example:

    class Category(MPTTModel):  # MPTTModel is a class from `django-mptt`, it allows to create tree structures with Categories as nodes
        parent = TreeForeignKey('self')  # foreign key to parent Category
        slug = ...
        ...

    class Photo(models.Model):
        category = models.ForeignKey('Category')
        slug = ...
        ...

Usually you create urlpattern like this:

    r'^gallery/(?P<category_slug>[-\w]+)/(?P<photo_slug>[-\w]+)$'
Therefore you restrict all your URLs to be as:

    /gallery/mountains/mountain-photo/
It is quite human-readable (and fast!), but you lose all Category's hierarchy. You'd better have URLs like this:

    /gallery/nature/mountains/mountain-photo/
    /gallery/nature/animals/frogs/green-frogs/green-frog-in-water/
    /gallery/portraits/jina/
These URLs are ["clean" / "semantic"](https://en.wikipedia.org/wiki/Semantic_URL), and django-clean-urls will help you to create them easily.

## Third-party app support
Django-clean-urls supports two main tree-structure apps for Django:

- django-mptt-urls
- django-treebeard

However, it's super easy to work with *any* hierarchy, no matter how you organize it.

## Requirements
- django (tested on but not restricted to v1.10)

## Example
TIP: All of the source code described below is available in *example* folder. It is a test project already set-up and ready-to-go, so you can `git clone` and play with it.
Let's create a gallery app with super-complicated hierarchy where we'll cover all use-cases of django-clean-urls.

    class Photographer(models.Model):
        state = models.CharField('usa state', max_length=2, choices=(
            ('CA', 'California'),
            ('CO', 'Colorado'),
            ('CT', 'Connecticut'),
            # enough for an example
        ))
        
