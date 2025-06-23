import string, random
from .models import ShortURL

def generate_shortcode(length=6):
    charset = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(charset, k=length))
        if not ShortURL.objects.filter(shortcode=code).exists():
            return code
