from invoke import run, task
import os.path

def _get_manage_dot_py(host):
    return '{path}/virtualenv/bin/python {path}/source/manage.py'.format(
            path='~/sites/%s' % host
    )


@task
def reset_database(host):
    _path = _get_manage_dot_py(host)
    if os.path.exists(_path):
        run('{manage_dot_py} flush --noinput'.format(
                manage_dot_py=_path
        ))
