from invoke import run, env, task


def _get_manage_dot_py(host):
    return '{path}/virtualenv/bin/python {path}/source/manage.py'.format(
            path='~/sites/%s' % host
    )


@task
def reset_database(host):
    run('{manage_dot_py} flush --noinput'.format(
            manage_dot_py=_get_manage_dot_py(host)
    ))
