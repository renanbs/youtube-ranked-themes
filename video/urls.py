from django.conf.urls import url
from .views import get_popular_themes


urlpatterns = [
    url(r'^$', get_popular_themes, name="themes"),

]
