# jep/urls.py
from django.urls import path
from django.conf.urls import url
from . import views

app_name = "basesite"

urlpatterns = [
    # ex: /
    path("", views.HomePageView.as_view(), name="index"),
    path("home/", views.HomePageView.as_view()),
    path("blog/", views.PostListView.as_view(), name="post_list"),
    url(
        r"(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<slug>[-\w]+)/$",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path("success/", views.successView, name="success"),
]
