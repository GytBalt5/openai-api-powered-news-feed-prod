from django.contrib.auth import get_user_model
from core.settings.dev import DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD


def create_super_user():
    # Create superuser (username and password are set in the settings).
    User = get_user_model()

    try:
        su = User.objects.get(username=DJANGO_SUPERUSER_USERNAME)
    except User.DoesNotExist:
        su = None

    if su:
        # Superuser exists.
        return su
    else:
        su = User.objects.create_superuser(
            username=DJANGO_SUPERUSER_USERNAME,
            password=DJANGO_SUPERUSER_PASSWORD,
            is_active=True,
            is_staff=True,
        )
        # Superuser created.
        return su
