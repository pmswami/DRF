from home.views import index, person, login
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("index/", index),
    path("person/", person),
    path("login/", login)
]
