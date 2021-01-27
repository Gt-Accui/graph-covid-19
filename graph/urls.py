from django.urls import path

from .views import SourceCreateView, SourceUpdateView
from .views import SourceFilterView, SourceDeleteView

urlpatterns = [
    path('', SourceFilterView.as_view(), name='index'),
    path('create/', SourceCreateView.as_view(), name='create'),
    path('update/<int:pk>/', SourceUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', SourceDeleteView.as_view(), name='delete'),
]
