from django.conf import settings as django_settings

class WebMonetizationMiddleware:
    """
    Middleware to add Web Monetization payment pointer to HTTP headers.
    
    This middleware automatically adds the 'Web-Monetization-Pointer' header to all
    HTTP responses if WEBMONETIZATION_PAYMENT_POINTER is configured in settings.py.
    
    Example configuration in settings.py:
        WEBMONETIZATION_PAYMENT_POINTER = '$ilp.example.com/your-payment-pointer'
        
        MIDDLEWARE = [
            ...
            'django_webmonetization.middleware.WebMonetizationMiddleware',
        ]
    
    Attributes:
        get_response: Function that gets the HTTP response.
        payment_pointer (str): The payment pointer configured in settings.py.
    """
    
    def __init__(self, get_response, settings=None):
        """
        Initialize the middleware.
        
        Args:
            get_response: Function that gets the HTTP response.
            settings: Optional settings object for testing.
        """
        self.get_response = get_response
        self.settings = settings or django_settings
        
        # Get payment pointer from settings
        if hasattr(self.settings, 'WEBMONETIZATION_PAYMENT_POINTER'):
            self.payment_pointer = getattr(self.settings, 'WEBMONETIZATION_PAYMENT_POINTER', None)
        elif hasattr(self.settings, 'payment_pointer'):
            self.payment_pointer = self.settings.payment_pointer
        else:
            self.payment_pointer = None

    def __call__(self, request):
        """
        Process the request and add the payment pointer to the response header.
        
        Args:
            request: The HttpRequest object.
            
        Returns:
            HttpResponse: The HTTP response with the monetization header added.
        """
        response = self.get_response(request)
        
        if self.payment_pointer:
            # For Django responses
            if hasattr(response, '__setitem__'):
                response['Web-Monetization-Pointer'] = self.payment_pointer
            # For our mock responses
            elif hasattr(response, 'headers'):
                response.headers['Web-Monetization-Pointer'] = self.payment_pointer
            
        return response
