# my_django_base/utils.py
import uuid
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views import View

def generate_unique_slug(model_instance, slugable_field_name, slug_field_name):
    """Generate a unique slug for a model instance"""
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = 1
    
    ModelClass = model_instance.__class__
    while ModelClass._default_manager.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{extension}"
        extension += 1
    
    return unique_slug

class AjaxRequiredMixin:
    """Mixin to require AJAX requests"""
    def dispatch(self, request, *args, **kwargs):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'AJAX request required'}, status=400)
        return super().dispatch(request, *args, **kwargs)

# Export constants for settings
DEFAULT_SETTINGS = {
    'PAGINATION_SIZE': 25,
    'MAX_UPLOAD_SIZE': 5242880,  # 5MB
    'DEFAULT_CACHE_TIMEOUT': 86400,  # 24 hours
}