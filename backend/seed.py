import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

User.objects.filter(username='admin').delete()

User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')
print("✅ Usuario admin creado desde cero con éxito")