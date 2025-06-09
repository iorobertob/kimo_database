from django.contrib import admin

# Register your models here.

from .models import Film, Institution

# admin.site.register(Film)
admin.site.register(Institution)

# This allows to add institutions at the time of adding a film 
# class InstitutionInline(admin.TabularInline):
# 	model = Institution

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):

	list_display = ('__str__', 'institution', 'movie_language', 'genre')

	list_filter = ('production_year', 'original_title')

	# inlines = [InstitutionInline]

	# pass



