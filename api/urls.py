from django.urls import path
from .views import FilmsView, FilmDetailView
from . import views


urlpatterns = [
    path('films/', FilmsView.as_view(), name='api_films'),
    path('film/<int:pk>', FilmDetailView.as_view(), name='api_film_detail'),

    # Institution endpoints
    path('institutions/', views.InstitutionListView.as_view(), name='institution-list'),
    path('institutions/<int:pk>/', views.InstitutionDetailView.as_view(), name='institution-detail'),
    
    # Film endpoints
    path('films-simplified/', views.FilmListView.as_view(), name='film-list'),
    path('films/<int:pk>/', views.FilmDetailView.as_view(), name='film-detail'),
    
    # Filtered film endpoints
    path('films/institution/<int:institution_id>/', views.FilmsByInstitutionView.as_view(), name='films-by-institution'),
    path('films/genre/<str:genre>/', views.FilmsByGenreView.as_view(), name='films-by-genre'),
    path('films/year/<int:year>/', views.FilmsByYearView.as_view(), name='films-by-year'),
    
    # Utility endpoints
    path('films/statistics/', views.film_statistics, name='film-statistics'),
    path('films/search/', views.search_films, name='film-search'),
]