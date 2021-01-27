from django.urls import path

from .views import ProcessFilterView, ProcessCreateView
from .views import ProcessUpdateView, ProcessDeleteView

urlpatterns = [
    path(
        '', ProcessFilterView.as_view(),
        name='process'),
    path(
        'create/', ProcessCreateView.as_view(),
        name='process_create'),
    path(
        'update/<int:pk>/', ProcessUpdateView.as_view(),
        name='process_update'),
    path(
        'delete/<int:pk>/', ProcessDeleteView.as_view(),
        name='process_delete'),
]
