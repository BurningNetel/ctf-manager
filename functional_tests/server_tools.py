from os import path
import subprocess

_cwd = path.dirname(path.abspath(__file__))


def reset_database(host):
    subprocess.check_call(
            ['fab', 'reset_database', '--host={}'.format(host)],
            cwd=_cwd
    )
