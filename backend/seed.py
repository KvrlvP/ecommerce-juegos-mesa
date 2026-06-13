import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})

user.set_password('admin12345')
user.is_staff = True
user.is_superuser = True
user.save()

print("✅ Contraseña de admin actualizada correctamente")