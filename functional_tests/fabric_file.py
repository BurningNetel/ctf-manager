from fabric.api import env, run


def _get_manage_dot_py(host):
    return '{path}/virtualenv/bin/python {path}/source/manage.py'.format(
            path='~/sites/%s' % host
    )


def reset_database():
    run('{manage_dot_py} flush --noinput'.format(
            manage_dot_py=_get_manage_dot_py(env.host)
    ))
