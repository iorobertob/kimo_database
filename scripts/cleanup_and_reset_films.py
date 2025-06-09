# Database cleanup and reset script
# Run this in Django shell: python manage.py shell

from django.db import transaction
from films.models import Film, Institution  # Replace with your actual app name

def cleanup_and_reset_films():
    """
    Clean up all film data and reset the database table
    """
    print("Starting database cleanup...")
    
    with transaction.atomic():
        # Get count before deletion
        film_count = Film.objects.count()
        print(f"Found {film_count} films to delete")
        
        # Delete all films
        Film.objects.all().delete()
        print("All films deleted successfully")
        
        # Reset auto-increment counter (PostgreSQL)
        from django.db import connection
        with connection.cursor() as cursor:
            # For PostgreSQL
            try:
                cursor.execute("ALTER SEQUENCE your_app_film_id_seq RESTART WITH 1;")
                print("PostgreSQL sequence reset")
            except:
                pass
            
            # For MySQL
            try:
                cursor.execute("ALTER TABLE your_app_film AUTO_INCREMENT = 1;")
                print("MySQL auto_increment reset")
            except:
                pass
            
            # For SQLite
            try:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='your_app_film';")
                print("SQLite sequence reset")
            except:
                pass
    
    print("Database cleanup completed!")

def check_encoding_issues():
    """
    Check for encoding issues in existing data
    """
    print("Checking for encoding issues...")
    
    problematic_films = []
    total_films = Film.objects.count()
    
    for film in Film.objects.all():
        issues = []
        
        # Check for underscore replacements
        if '_' in film.original_title:
            issues.append(f"Underscores in title: {film.original_title}")
        
        if film.director and '_' in film.director:
            issues.append(f"Underscores in director: {film.director}")
        
        # Check for other encoding issues
        text_fields = [
            film.original_title, film.english_title, film.director,
            film.producer, film.brief_introduction_en, film.synopsis_en
        ]
        
        for field_value in text_fields:
            if field_value:
                # Look for common encoding issue patterns
                if any(char in field_value for char in ['�', '?', '\\x']):
                    issues.append(f"Encoding issues detected in: {field_value[:50]}...")
        
        if issues:
            problematic_films.append({
                'id': film.id,
                'title': film.original_title,
                'issues': issues
            })
    
    print(f"Found {len(problematic_films)} films with potential encoding issues out of {total_films} total")
    
    # Show first 10 problematic films
    for film in problematic_films[:10]:
        print(f"Film ID {film['id']}: {film['title']}")
        for issue in film['issues']:
            print(f"  - {issue}")
    
    return problematic_films

def fix_lithuanian_characters():
    """
    Attempt to fix common Lithuanian character issues
    """
    print("Attempting to fix Lithuanian character issues...")
    
    # Common replacements for Lithuanian characters
    replacements = {
        '_': {  # If underscores were used as replacement
            'a_': 'ą',
            'c_': 'č',
            'e_': 'ę',
            'e__': 'ė',
            'i_': 'į',
            's_': 'š',
            'u_': 'ų',
            'u__': 'ū',
            'z_': 'ž',
            # Uppercase
            'A_': 'Ą',
            'C_': 'Č',
            'E_': 'Ę',
            'E__': 'Ė',
            'I_': 'Į',
            'S_': 'Š',
            'U_': 'Ų',
            'U__': 'Ū',
            'Z_': 'Ž',
        }
    }
    
    fixed_count = 0
    
    with transaction.atomic():
        for film in Film.objects.all():
            updated = False
            
            # Fix text fields
            text_fields = [
                'original_title', 'english_title', 'director', 'producer',
                'brief_introduction_en', 'synopsis_en', 'content_summary_en'
            ]
            
            for field_name in text_fields:
                field_value = getattr(film, field_name, '')
                if field_value:
                    original_value = field_value
                    
                    # Apply replacements
                    for pattern, replacement in replacements['_'].items():
                        field_value = field_value.replace(pattern, replacement)
                    
                    if field_value != original_value:
                        setattr(film, field_name, field_value)
                        updated = True
            
            if updated:
                film.save()
                fixed_count += 1
    
    print(f"Fixed {fixed_count} films with Lithuanian character issues")

# Usage functions
if __name__ == "__main__":
    print("Database Management Script")
    print("1. To check for encoding issues: check_encoding_issues()")
    print("2. To clean up all data: cleanup_and_reset_films()")
    print("3. To fix Lithuanian characters: fix_lithuanian_characters()")
    print("\nRun these functions individually based on your needs.")

# Quick usage examples:
"""
# In Django shell (python manage.py shell):

# 1. Check what's wrong with current data
from your_app.cleanup_script import check_encoding_issues
problematic_films = check_encoding_issues()

# 2. Clean everything and start fresh
from your_app.cleanup_script import cleanup_and_reset_films
cleanup_and_reset_films()

# 3. Try to fix existing data without deleting
from your_app.cleanup_script import fix_lithuanian_characters
fix_lithuanian_characters()
"""