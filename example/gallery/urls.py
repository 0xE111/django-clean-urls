from django.conf.urls import url

from clean_urls.views import CleanURLHandler

from .models import Photographer
from .views import HomeView, PhotographerView


app_name = 'gallery'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),  # home page - just to show list of photographers
    url(
        r'^(?P<slug>.+)$',  # very generic regex - captures everything except empty string
        CleanURLHandler(  # this class will do all dirty work for us
            (Photographer.objects.all(), PhotographerView.as_view()),  # clean url will start with Photographer's slug and call PhotographerView
        ),
        name='generic'  # needed for reverse url resolution; call it "generic" because this url can point to many different objects
    ),
]