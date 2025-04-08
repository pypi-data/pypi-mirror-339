from django import template
from django.conf import settings as django_settings
from django.utils.safestring import mark_safe

register = template.Library()

def get_payment_pointer(settings=None):
    """
    Get the payment pointer from settings.
    
    Args:
        settings: Optional settings object for testing.
        
    Returns:
        str: The payment pointer or None if not configured.
    """
    settings = settings or django_settings
    # For Django settings
    if hasattr(settings, 'WEBMONETIZATION_PAYMENT_POINTER'):
        return getattr(settings, 'WEBMONETIZATION_PAYMENT_POINTER', None)
    # For our mock settings
    elif hasattr(settings, 'payment_pointer'):
        return settings.payment_pointer
    return None

@register.simple_tag
def webmonetization_meta(settings=None):
    """
    Template tag that generates the Web Monetization meta tag.
    
    This tag generates the HTML meta tag needed to enable Web Monetization
    on the page. The payment pointer is obtained from the
    WEBMONETIZATION_PAYMENT_POINTER setting in settings.py.
    
    Example usage in a template:
        {% load webmonetization %}
        <!DOCTYPE html>
        <html>
        <head>
            {% webmonetization_meta %}
            ...
        </head>
        
    Args:
        settings: Optional settings object for testing.
        
    Returns:
        str: The formatted HTML meta tag with the payment pointer, or an empty
            string if no payment pointer is configured.
    """
    payment_pointer = get_payment_pointer(settings)
    if payment_pointer:
        return mark_safe(f'<meta name="monetization" content="{payment_pointer}">')
    return ''
