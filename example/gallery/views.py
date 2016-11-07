from django.views.generic import DetailView, ListView

from .models import Photographer


class HomeView(ListView):
    model = Photographer

    template_name = 'gallery/home.html'


class PhotographerView(DetailView):
    template_name = 'gallery/photographer.html'

    def dispatch(self, *args, **kwargs):  # already resolved instance here!
        self.instance = kwargs.pop('instance')  # save instance
        return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.instance  # use saved instance


class CategoryView(DetailView):
    template_name = 'gallery/category.html'

    def dispatch(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.instance


class PhotoView(DetailView):
    template_name = 'gallery/photo.html'

    def dispatch(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.instance
