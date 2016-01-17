from os import path
import subprocess

_cwd = path.dirname(path.abspath(__file__))


def reset_database(host):
    subprocess.check_call(
            ['invoke', 'reset_database', '--host=%s' % host],
            cwd=_cwd
    )
