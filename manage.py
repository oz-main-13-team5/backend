#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()  # .env.prod 파일 읽기 (os.environ.setdefault 환경변수)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def run_dev():
    os.environ["ENV_FILE"] = ".env.dev"
    from django.core.management import execute_from_command_line

    execute_from_command_line([sys.argv[0], "runserver"])


def run_prod():
    os.environ["ENV_FILE"] = ".env.prod"
    from django.core.management import execute_from_command_line

    execute_from_command_line([sys.argv[0], "runserver", "0.0.0.0:8000"])


if __name__ == "__main__":
    main()
