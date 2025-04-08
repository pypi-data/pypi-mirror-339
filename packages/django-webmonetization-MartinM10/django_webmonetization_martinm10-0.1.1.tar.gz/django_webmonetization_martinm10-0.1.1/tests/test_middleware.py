from django_webmonetization.middleware import WebMonetizationMiddleware

class MockSettings:
    def __init__(self, payment_pointer=None):
        self.payment_pointer = payment_pointer

class MockRequest:
    pass

class MockResponse:
    def __init__(self):
        self.headers = {}

def test_middleware_with_payment_pointer():
    # Setup
    settings = MockSettings(payment_pointer='$ilp.example.com/test')
    middleware = WebMonetizationMiddleware(get_response=lambda r: MockResponse(), settings=settings)
    request = MockRequest()
    
    # Execute
    response = middleware(request)
    
    # Assert
    assert response.headers['Web-Monetization-Pointer'] == '$ilp.example.com/test'

def test_middleware_without_payment_pointer():
    # Setup
    settings = MockSettings(payment_pointer=None)
    middleware = WebMonetizationMiddleware(get_response=lambda r: MockResponse(), settings=settings)
    request = MockRequest()
    
    # Execute
    response = middleware(request)
    
    # Assert
    assert 'Web-Monetization-Pointer' not in response.headers 