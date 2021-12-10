from django.urls import path

from . import views
app_name="ency"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.create_entry,name="createentry"),
    path("random/", views.randomx,name="random"),
    path("<str:name>/",views.view_page, name="view_page"),
    path("nav", views.nav, name = "nav"),
    path("<str:name>/edit/", views.editentry, name ="edit")
]
