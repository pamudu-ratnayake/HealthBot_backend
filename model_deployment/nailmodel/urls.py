from django.urls import path
from .views import NailDIdentifier

urlpatterns = [
    path('disease', NailDIdentifier.get_disease_category, name='disease')
]