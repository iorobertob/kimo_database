from django.urls import path
from . import views

urlpatterns = [
	# path('', views.index, name = 'index'),
	path('', views.FilmListView.as_view(), name = 'films-list'),
	path('film/<int:pk>', views.FilmDetailView.as_view(), name='film-detail'),
]
