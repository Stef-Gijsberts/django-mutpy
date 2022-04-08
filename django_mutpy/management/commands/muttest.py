"""Contains the 'manage.py muttest' command."""
import importlib.util
import pkgutil

import mutpy.commandline
from django.conf import settings
from django.core.management import BaseCommand
from django.core.management import CommandError
from django.test.utils import setup_databases
from django.test.utils import setup_test_environment
from django.test.utils import teardown_databases
from django.test.utils import teardown_test_environment


def get_leaf_modules(parent_name):
    """Recursively get a list of all non-package modules in a package."""
    parent_path = importlib.import_module(parent_name).__path__

    for _, child_name, is_package in pkgutil.iter_modules(parent_path):
        child_full_name = f"{parent_name}.{child_name}"

        if is_package:
            yield from get_leaf_modules(child_full_name)
        else:
            yield child_full_name


def is_target(name: str) -> bool:
    """Return true if and only if the module is a test target."""
    parts = name.split(".")
    return ("migrations" not in parts) and ("tests" not in parts)


def is_test(name: str) -> bool:
    """Return true if and only if the module is a test module."""
    return name.split(".")[-1].startswith("test")


def run_mutpy_on_app(app):
    """Let MutPy run mutations tests on a single Django app."""
    setup_test_environment()
    old_config = setup_databases(verbosity=1, interactive=True)

    leaf_modules = list(get_leaf_modules(app))

    target_modules = [name for name in leaf_modules if is_target(name)]
    test_modules = [name for name in leaf_modules if is_test(name)]

    mutpy_options = [
        "--target",
        *target_modules,
        "--unit-test",
        *test_modules,
        "--show-mutants",
    ]
    print(mutpy_options)
    mutpy.commandline.main(mutpy_options)

    teardown_databases(old_config, verbosity=1)
    teardown_test_environment()


def ensure_apps_are_installed(apps) -> None:
    """Raise an exception if not all given apps are installed. Do nothing otherwise."""
    installed_apps = settings.INSTALLED_APPS
    missing_apps = set(apps) - set(installed_apps)

    if missing_apps:
        raise CommandError(
            f"Apps {missing_apps} are not among INSTALLED_APPS {installed_apps}"
        )


class Command(BaseCommand):
    """This command runs MutPy against one or more Django apps."""

    can_import_settings = True

    def add_arguments(self, parser):
        """Define cmd arguments."""
        parser.add_argument("app", nargs="+", type=str)

    def handle(self, *args, **options):
        """Run MutPy against the provided apps."""
        apps = options["app"]

        ensure_apps_are_installed(apps)

        for app in apps:
            run_mutpy_on_app(app)
