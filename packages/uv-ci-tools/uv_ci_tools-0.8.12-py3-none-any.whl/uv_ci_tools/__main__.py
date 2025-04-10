import sys

from uv_ci_tools import app


def main():
    app.APP.__call__(sys.argv[1:], print_error=False, exit_on_error=False)
