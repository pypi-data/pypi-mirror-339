import pathlib
import subprocess

from uv_ci_tools.lib import ci, util


def get_git():
    git_exe_path = util.get_exe_path('git')

    def git(*args: util.StrOrBytesPath, no_check: bool = False):
        subprocess.run([git_exe_path, *args], check=not no_check)

    return git


def push(*paths: pathlib.Path, message: str, ci_ctx: ci.Context):
    if ci_ctx.password is None:
        msg = 'Cannot git push without password'
        raise RuntimeError(msg)

    git = get_git()
    origin_name = 'origin'
    origin_url = (
        f'https://{ci_ctx.username}:{ci_ctx.password}'
        f'@{ci_ctx.repository_host}/{ci_ctx.project_path}.git'
    )
    git('config', 'user.name', ci_ctx.username)
    git('config', 'user.email', ci_ctx.email)
    git('remote', 'remove', origin_name, no_check=True)
    git('remote', 'add', origin_name, origin_url)
    git('add', *paths)
    git('commit', '-m', message)
    git('push', origin_name, f'HEAD:{ci_ctx.commit_ref_name}', '-o', 'ci.skip')
