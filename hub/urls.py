from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
path('webhook/github/', views.github_webhook, name='github_webhook'),
]