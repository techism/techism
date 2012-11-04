#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # create test fixture first
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        os.chdir("test-utils")
        execfile("transform_fixture.py")
        os.chdir("..")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techism.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
