from django_webmonetization.templatetags.webmonetization import webmonetization_meta

class MockSettings:
    def __init__(self, payment_pointer=None):
        self.payment_pointer = payment_pointer

def test_template_tag_with_payment_pointer():
    # Setup
    settings = MockSettings(payment_pointer='$ilp.example.com/test')
    
    # Execute
    result = webmonetization_meta(settings=settings)
    
    # Assert
    assert result == '<meta name="monetization" content="$ilp.example.com/test">'

def test_template_tag_without_payment_pointer():
    # Setup
    settings = MockSettings(payment_pointer=None)
    
    # Execute
    result = webmonetization_meta(settings=settings)
    
    # Assert
    assert result == '' 