from django.conf.urls import url

from clean_urls.views import CleanURLHandler

from .models import Photographer, Category, Photo
from .views import HomeView, PhotographerView, CategoryView, PhotoView


app_name = 'gallery'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),  # home page - just to show list of photographers
    url(
        r'^(?P<slug>([-\w]+/)+)$',  # very generic regex
        CleanURLHandler(  # this class will do all dirty work for us
            (Photographer.objects.all(), PhotographerView.as_view()),  # clean url will start with Photographer's slug and call PhotographerView
            (Category.objects.all(), CategoryView.as_view()),  # here we state that Photographer may contain a Category within
            (Photo.objects.all(), PhotoView.as_view()),  # and Category may contain Photos within
            # ... don't stop! :)
        ),
        name='generic'  # needed for reverse url resolution; call it "generic" because this url can point to many different objects
    ),
]