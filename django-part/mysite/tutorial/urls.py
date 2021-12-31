from django.urls import path, re_path

from .views import EchoView, FibAndGetJasonView, FibAndPostJasonView

urlpatterns = [
    re_path(r'^tutorial/?$', EchoView.as_view()),
    re_path(r'^fibonacci/?$', FibAndPostJasonView.as_view()),
    re_path(r'^logs/?$', FibAndGetJasonView.as_view()),
]
