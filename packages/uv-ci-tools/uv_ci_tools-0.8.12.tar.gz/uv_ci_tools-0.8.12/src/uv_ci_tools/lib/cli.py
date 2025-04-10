def _app(*, name: str | None):
    import cyclopts

    import uv_ci_tools

    app = cyclopts.App(name=name, version=uv_ci_tools.__version__)
    app['--help'].group = 'Extra'
    app['--version'].group = 'Extra'
    return app


def _format_command_name(name: str):
    return name.split('.')[-2].replace('_', '-')


def main_app():
    return _app(name=None)


def sub_app(name: str):
    return _app(name=_format_command_name(name))
