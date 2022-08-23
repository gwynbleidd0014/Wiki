from django.urls import path

from . import views
from . import util

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("random/", views.random, name="random"),
    path("<page>/edit", views.edit, name="edit"),
    path("<entrie>/", views.entries, name="pages"),

]

