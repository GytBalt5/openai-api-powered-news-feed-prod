import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.settings_for_testing")
django.setup()
