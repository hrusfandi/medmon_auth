import os
import django
from django.contrib.auth.models import ContentType

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

django.setup()


new_ct, created = ContentType.objects.get_or_create(app_label='external',
                                                    model='ms')
