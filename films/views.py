from django.shortcuts import render

# Create your views here.

from .models import Film, Institution
from django.views import generic

# DEPRECATED
def index(request):
	"""View function for home page of this site."""

	# Generate counts of som of the main objects
	num_films = Film.objects.all().count()
	num_institutions = Institution.objects.all().count()

	# This year's films
	num_films_thisyear = Film.objects.filter(production_year__gte = 2025).count()

	context = {

		'films' : Film.objects.all()

	}

	return render(request, 'index.html', context = context)


class FilmListView(generic.ListView):
	model = Film

	context_object_name = 'films'

	# Get 5 films containing the title war
	# queryset = Film.objects.filter(original_title__icontains='war')[:5] 

	# specify custom template file name
	template_name = 'index.html'

	paginate_by = 20


class FilmDetailView(generic.DetailView):
	model = Film

	context_object_name = 'film'
	template_name = 'film_detail.html'

	# def film_detail_view(request, primary_key):