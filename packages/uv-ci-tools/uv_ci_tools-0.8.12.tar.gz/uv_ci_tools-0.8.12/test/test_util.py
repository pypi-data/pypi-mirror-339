import os

from uv_ci_tools.lib import util


def test_set_env():
    name = 'MY_VARIABLE_687043857'
    assert os.getenv(name) is None
    with util.set_env(name, value=None):
        assert os.getenv(name) is None
    with util.set_env(name, value='VALUE'):
        assert os.getenv(name) == 'VALUE'
        with util.set_env(name, value=None):
            assert os.getenv(name) is None
        assert os.getenv(name) == 'VALUE'
    assert os.getenv(name) is None
