import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.settings_for_tests")
django.setup()
