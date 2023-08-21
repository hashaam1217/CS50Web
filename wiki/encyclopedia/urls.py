from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_name>/", views.pages, name="pages"),
    path("Search/", views.Search, name="Search"),
    path("NewPage/", views.NewPage, name="NewPage"),
    path("wiki/<str:page_name>/EditPage/", views.EditPage, name="EditPage")
]
