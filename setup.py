# coding=utf8
from setuptools import setup

setup(
    name='Kuyruk-Requeue',
    version="1.1.1",
    author=u'Cenk Altı',
    author_email='cenkalti@gmail.com',
    keywords='kuyruk requeue',
    url='https://github.com/cenkalti/kuyruk-requeue',
    py_modules=["kuyruk_requeue"],
    install_requires=[
        'kuyruk>=3.0.0',
        'redis>=2.10.3',
    ],
    entry_points={'kuyruk.config': 'requeue = kuyruk_requeue:CONFIG',
                  'kuyruk.commands': 'requeue = kuyruk_requeue:command'},
    description='Save failed tasks to Redis and requeue them.',
    long_description=open('README.md').read(),
)
