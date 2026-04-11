import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omni_platform_project.settings')
django.setup()
from django.contrib.auth.models import User

username = 'Rekha'
password = '2a2211@rekha'
try:
    u = User.objects.get(username=username)
    u.set_password(password)
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print("Rekha updated to superuser!")
except User.DoesNotExist:
    User.objects.create_superuser(username, 'rekha@example.com', password)
    print("Rekha created as superuser!")
