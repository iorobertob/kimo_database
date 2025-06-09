from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import generics, filters, status
from rest_framework.decorators import api_view

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from films.models import Institution, Film
from .serializers import (
    InstitutionSerializer, 
    FilmListSerializer, 
    FilmDetailSerializer, 
    FilmCreateUpdateSerializer
)

class InstitutionListView(generics.ListCreateAPIView):
    """List all institutions or create a new one"""
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class InstitutionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an institution"""
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class FilmsView(APIView):
    def get(self, request):
        films = Film.objects.all()
        serializer = FilmListSerializer(films, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FilmListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class FilmListView(generics.ListCreateAPIView):
    """List all films or create a new one"""
    queryset = Film.objects.select_related('institution', 'created_by').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering options
    filterset_fields = {
        'genre': ['exact', 'in'],
        'project_type': ['exact', 'in'],
        'production_year': ['exact', 'gte', 'lte'],
        'institution': ['exact'],
        'color': ['exact'],
        'general_type': ['exact'],
    }
    
    # Search functionality
    search_fields = [
        'original_title', 'english_title', 'director', 'producer',
        'keywords', 'brief_introduction_en', 'synopsis_en'
    ]
    
    # Ordering options
    ordering_fields = [
        'original_title', 'production_year', 'created_at', 'updated_at'
    ]
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FilmCreateUpdateSerializer
        return FilmListSerializer


class FilmDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a film"""
    queryset = Film.objects.select_related('institution', 'created_by').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return FilmCreateUpdateSerializer
        return FilmDetailSerializer


class FilmsByInstitutionView(generics.ListAPIView):
    """List all films by a specific institution"""
    serializer_class = FilmListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        institution_id = self.kwargs['institution_id']
        return Film.objects.filter(institution_id=institution_id).select_related('institution', 'created_by')


class FilmsByGenreView(generics.ListAPIView):
    """List all films by genre"""
    serializer_class = FilmListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        genre = self.kwargs['genre']
        return Film.objects.filter(genre=genre).select_related('institution', 'created_by')


class FilmsByYearView(generics.ListAPIView):
    """List all films by production year"""
    serializer_class = FilmListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        year = self.kwargs['year']
        return Film.objects.filter(production_year=year).select_related('institution', 'created_by')


@api_view(['GET'])
def film_statistics(request):
    """Get basic statistics about films"""
    from django.db.models import Count, Min, Max
    
    stats = Film.objects.aggregate(
        total_films=Count('id'),
        earliest_year=Min('production_year'),
        latest_year=Max('production_year'),
    )
    
    # Genre distribution
    genre_stats = Film.objects.values('genre').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Institution distribution
    institution_stats = Film.objects.values(
        'institution__name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    return Response({
        'overview': stats,
        'by_genre': list(genre_stats),
        'by_institution': list(institution_stats)
    })


@api_view(['GET'])
def search_films(request):
    """Advanced search endpoint"""
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search across multiple fields
    films = Film.objects.filter(
        Q(original_title__icontains=query) |
        Q(english_title__icontains=query) |
        Q(director__icontains=query) |
        Q(producer__icontains=query) |
        Q(keywords__icontains=query) |
        Q(brief_introduction_en__icontains=query) |
        Q(synopsis_en__icontains=query)
    ).select_related('institution', 'created_by')
    
    serializer = FilmListSerializer(films, many=True)
    return Response({
        'count': films.count(),
        'results': serializer.data
    })

