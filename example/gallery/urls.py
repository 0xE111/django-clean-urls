from django.conf.urls import url

from clean_urls.views import CleanURLHandler

from .models import Photographer, Category
from .views import HomeView, PhotographerView, CategoryView


app_name = 'gallery'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),  # home page - just to show list of photographers
    url(
        r'^(?P<slug>([-\w]+/)+)$',  # very generic regex
        CleanURLHandler(  # this class will do all dirty work for us
            (Photographer.objects.all(), PhotographerView.as_view()),  # clean url will start with Photographer's slug and call PhotographerView
            (Category.objects.all(), CategoryView.as_view()),
        ),
        name='generic'  # needed for reverse url resolution; call it "generic" because this url can point to many different objects
    ),
]