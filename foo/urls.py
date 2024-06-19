from django.urls import path

from foo.views import main_view


urlpatterns = [
    path('', main_view),
]
