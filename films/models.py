from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Institution(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name

class Film(models.Model):
    # General Data (Section 1)
    institution 			= models.ForeignKey(Institution, on_delete=models.CASCADE)
    project_number 			= models.CharField(max_length=50, blank=True)
    original_title 			= models.CharField(max_length=255)
    english_title 			= models.CharField(max_length=255, blank=True)
    original_subtitle		= models.CharField(max_length=255, blank=True)
    english_subtitle 		= models.CharField(max_length=255, blank=True)
    production_year 		= models.IntegerField()
    director 				= models.CharField(max_length=255)
    producer 				= models.CharField(max_length=255, blank=True)
    co_producer 			= models.CharField(max_length=255, blank=True)
    instructor_supervisor 	= models.CharField(max_length=255, blank=True)
    movie_language 			= models.CharField(max_length=100)
    subtitle_languages 		= models.CharField(max_length=255, blank=True)
    working_title 			= models.CharField(max_length=255, blank=True)
    complementary_data 		= models.TextField(blank=True)
    
    GENRE_CHOICES = [
        ('drama', 'Drama'),
        ('documentary', 'Documentary'),
        ('comedy', 'Comedy'),
        ('tragedy', 'Tragedy'),
        ('other', 'Other'),
    ]
    genre 		= models.CharField(max_length=20, choices=GENRE_CHOICES)
    genre_other = models.CharField(max_length=100, blank=True)
    
    PROJECT_TYPE_CHOICES = [
        ('short_film', 'Short Film'),
        ('animation', 'Animation'),
        ('tv_program', 'TV Program'),
        ('newsreel', 'Newsreel'),
        ('advertising', 'Advertising'),
        ('other', 'Other'),
    ]
    project_type 		= models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)
    project_type_other 	= models.CharField(max_length=100, blank=True)
    
    main_cast 			= models.TextField(blank=True)
    persons_shown 		= models.TextField(blank=True)  # For documentaries
    persons_speaking 	= models.TextField(blank=True)  # For documentaries
    persons_spoken_about= models.TextField(blank=True)
    additional_info 	= models.TextField(blank=True)
    doi 				= models.CharField(max_length=255, blank=True)
    streaming_link 		= models.URLField(blank=True)
    additional_webpage 	= models.URLField(blank=True)
    archive_notes 		= models.TextField(blank=True)
    
    # Production Data (Section 2)
    production_country 	= models.CharField(max_length=100, blank=True)
    production_date 	= models.DateField(null=True, blank=True)
    production_company 	= models.CharField(max_length=255, blank=True)
    cooperation_partners= models.TextField(blank=True)
    supported_by 		= models.TextField(blank=True)
    inside_locations 	= models.TextField(blank=True)
    outside_locations 	= models.TextField(blank=True)
    number_of_episodes 	= models.IntegerField(null=True, blank=True)
    
    # Technical Data (Section 3)
    COLOR_CHOICES = [
        ('black_white', 'Black and White'),
        ('color', 'Color'),
        ('other', 'Other'),
    ]
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    
    TYPE_CHOICES = [
        ('film', 'Film'),
        ('digital_video', 'Digitally on Video'),
        ('digital_ramdisk', 'Digitally on Ramdisk'),
        ('other', 'Other'),
    ]
    general_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    FILM_FORMAT_CHOICES = [
        ('8mm', '8mm'),
        ('other', 'Other'),
    ]
    film_format = models.CharField(max_length=20, choices=FILM_FORMAT_CHOICES, blank=True)
    
    DIGITAL_FORMAT_CHOICES = [
        ('digibeta', 'Digibeta'),
        ('dv', 'DV'),
        ('mini_dv', 'Mini DV'),
        ('dvcam', 'DVCAM'),
        ('dvcpro', 'DVCPRO'),
        ('hdcam', 'HDCAM'),
        ('digital_8', 'Digital 8 (8mm)'),
        ('other', 'Other'),
    ]
    digital_format = models.CharField(max_length=20, choices=DIGITAL_FORMAT_CHOICES, blank=True)
    
    RATIO_CHOICES = [
        ('4:3', '4:3'),
        ('16:9', '16:9'),
        ('16:10', '16:10'),
        ('21:9', '21:9'),
        ('other', 'Other'),
    ]
    screen_ratio = models.CharField(max_length=10, choices=RATIO_CHOICES, blank=True)
    
    SOUND_CHOICES = [
        ('mono', 'Mono'),
        ('stereo', 'Stereo'),
        ('dolby_5_1', 'Dolby 5.1 Surround'),
        ('other', 'Other'),
    ]
    sound_format = models.CharField(max_length=20, choices=SOUND_CHOICES, blank=True)
    
    running_time = models.CharField(max_length=10, blank=True)  # Format: mm:ss
    
    # Content Data (Section 4)
    brief_introduction_en 	= models.TextField()
    brief_introduction_local= models.TextField(blank=True)
    logline 				= models.TextField(blank=True)
    synopsis_en 			= models.TextField()
    synopsis_local 			= models.TextField(blank=True)
    content_summary_en 		= models.TextField()
    content_summary_local 	= models.TextField(blank=True)
    keywords 				= models.TextField()
    time_of_movie 			= models.CharField(max_length=255, blank=True)
    target_audience 		= models.CharField(max_length=255)
    
    # Distribution Data (Section 5)
    copyright_owners 		= models.TextField(blank=True)
    access_levels 			= models.CharField(max_length=255, blank=True)
    trailer 				= models.FileField(upload_to='trailers/', blank=True)
    poster 					= models.ImageField(upload_to='posters/', blank=True)
    logo 					= models.ImageField(upload_to='logos/', blank=True)
    distributor 			= models.CharField(max_length=255, blank=True)
    final_credits 			= models.CharField(max_length=255, blank=True)
    premiere_info 			= models.TextField(blank=True)
    festival_participation 	= models.TextField(blank=True)
    festival_prizes 		= models.TextField(blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_films')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # ordering = ['-created_at']
        ordering = ['original_title']
        indexes = [
            models.Index(fields=['original_title']),
            models.Index(fields=['production_year']),
            models.Index(fields=['genre']),
            models.Index(fields=['project_type']),
        ]
    
    def __str__(self):
        return f"{self.original_title} ({self.production_year})"


    
    @property
    def thumbnail_url(self):
        if self.poster:
            return self.poster.url
        return '/static/images/no-poster.jpg'