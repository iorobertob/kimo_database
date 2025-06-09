#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django
import csv
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kimo_1.settings')
django.setup()

from films.models import Film, Institution
from django.contrib.auth import get_user_model

User = get_user_model()

def parse_duration(duration_str):
    """Parse duration string like '23:36' or '25:17:00' to minutes:seconds format"""
    if not duration_str or duration_str == 'К':
        return ''
    
    # Handle different duration formats
    parts = duration_str.split(':')
    if len(parts) == 2:
        # Format: mm:ss
        return duration_str
    elif len(parts) == 3:
        # Format: hh:mm:ss, convert to mm:ss
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = parts[2]
        total_minutes = hours * 60 + minutes
        return f"{total_minutes}:{seconds}"
    
    return duration_str

def clean_field(value):
    """Clean field value, handle Lithuanian characters and empty values"""
    if not value or value.strip() == '':
        return ''
    return value.strip()

def import_films_from_csv():
    # Get or create default institution
    institution, created = Institution.objects.get_or_create(
        code='LMTA',
        defaults={'name': 'Lietuvos muzikos ir teatro akademija'}
    )
    
    # Get or create default user for created_by field
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'System',
            'last_name': 'Administrator'
        }
    )
    
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'studentai.csv')
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        # Read CSV with proper handling of Lithuanian characters and semicolon delimiter
        csv_reader = csv.DictReader(file, delimiter=';')
        
        films_created = 0
        films_skipped = 0
        
        for row in csv_reader:
            try:
                # Extract basic information
                base_title = clean_field(row.get('Pavadinimas', ''))
                if not base_title:
                    print(f"Skipping row with no title")
                    films_skipped += 1
                    continue
                
                director = clean_field(row.get('Režisierius', ''))
                
                # Create unique title by appending director name if film already exists
                original_title = base_title
                if Film.objects.filter(original_title=original_title).exists():
                    if director:
                        original_title = f"{base_title} ({director})"
                        print(f"Film '{base_title}' already exists, creating as '{original_title}'")
                    else:
                        print(f"Film '{base_title}' already exists and no director specified, skipping")
                        films_skipped += 1
                        continue
                
                # Double-check if the modified title also exists
                if Film.objects.filter(original_title=original_title).exists():
                    print(f"Film '{original_title}' already exists, skipping")
                    films_skipped += 1
                    continue
                
                production_year_str = clean_field(row.get('Metai', ''))
                try:
                    production_year = int(production_year_str) if production_year_str else 1991
                except ValueError:
                    production_year = 1991
                
                duration = parse_duration(clean_field(row.get('Trukmė', '')))
                genre_field = clean_field(row.get('Rūšis', ''))
                task_field = clean_field(row.get('Užduotis', ''))
                # director already extracted above
                supervisor = clean_field(row.get('Kurso vadovas', ''))
                course = clean_field(row.get('Kursas', ''))
                original_format = clean_field(row.get('originalus formatas', ''))
                keywords = clean_field(row.get('Raktiniai žodžiai', ''))
                
                # Map genre - default to 'other' since Lithuanian genres don't match our choices
                genre = 'other'
                if 'dokumentas' in genre_field.lower():
                    genre = 'documentary'
                elif 'drama' in genre_field.lower():
                    genre = 'drama'
                elif 'komedija' in genre_field.lower():
                    genre = 'comedy'
                
                # Map project type - default to 'short_film'
                project_type = 'short_film'
                if 'animacija' in task_field.lower():
                    project_type = 'animation'
                elif 'tv' in task_field.lower():
                    project_type = 'tv_program'
                elif 'reklama' in task_field.lower():
                    project_type = 'advertising'
                
                # Map technical format
                general_type = 'other'
                if 'VHS' in original_format:
                    general_type = 'digital_video'
                elif 'film' in original_format.lower():
                    general_type = 'film'
                
                # Create Film instance
                film = Film.objects.create(
                    institution=institution,
                    original_title=original_title,
                    english_title='',  # Not provided in CSV
                    production_year=production_year,
                    director=director,
                    instructor_supervisor=supervisor,
                    movie_language='Lithuanian',
                    genre=genre,
                    genre_other=genre_field if genre == 'other' else '',
                    project_type=project_type,
                    project_type_other=task_field if project_type == 'other' else '',
                    general_type=general_type,
                    running_time=duration,
                    brief_introduction_en=f"Lithuanian student film from {production_year}",
                    synopsis_en=f"Student film directed by {director}" + (f", supervised by {supervisor}" if supervisor else ""),
                    content_summary_en=f"Course: {course}" if course else "Student film project",
                    keywords=keywords,
                    target_audience='Academic/Educational',
                    created_by=user,
                    # Additional fields from CSV
                    complementary_data=f"Original format: {original_format}" + (f", Course: {course}" if course else ""),
                    archive_notes=f"Imported from CSV. Genre: {genre_field}, Task: {task_field}",
                )
                
                print(f"Created film: {original_title} ({production_year})")
                films_created += 1
                
            except Exception as e:
                print(f"Error processing row: {e}")
                print(f"Row data: {row}")
                films_skipped += 1
                continue
    
    print(f"\nImport completed:")
    print(f"Films created: {films_created}")
    print(f"Films skipped: {films_skipped}")

if __name__ == '__main__':
    import_films_from_csv()