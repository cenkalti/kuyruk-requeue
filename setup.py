# coding=utf8
from setuptools import setup

setup(
    name='Kuyruk-Requeue',
    version="1.2.0",
    author=u'Cenk Altı',
    author_email='cenkalti@gmail.com',
    keywords='kuyruk requeue',
    url='https://github.com/cenkalti/kuyruk-requeue',
    py_modules=["kuyruk_requeue"],
    install_requires=[
        'kuyruk>=8.0.0',
        'redis>=2.10.3',
    ],
    entry_points={'kuyruk.config': 'requeue = kuyruk_requeue:CONFIG',
                  'kuyruk.commands': 'requeue = kuyruk_requeue:command'},
    description='Save failed tasks to Redis and requeue them.',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Object Brokering',
        'Topic :: System :: Distributed Computing',
    ],
)
