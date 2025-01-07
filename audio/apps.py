from django.apps import AppConfig


class AudioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audio'
    
    def ready(self): 
        import audio.models