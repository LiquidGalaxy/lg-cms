#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lg_cms.settings")

    # Protect from a specific Denial of Service Attack.
    # https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#python-options
    # http://www.ocert.org/advisories/ocert-2011-003.html
    os.environ.setdefault("PYTHONHASHSEED", "random")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
