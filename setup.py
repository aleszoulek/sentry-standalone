import os
from setuptools import setup, find_packages


try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
    long_description = f.read().strip()
    f.close()
except IOError:
    long_description = None

setup(
    name='sentry-standalone',
    version='0.2',
    url="http://github.com/aleszoulek/sentry-standalone",
    description='Sentry client without django dependency',
    long_description=long_description,
    author='Ales Zoulek',
    author_email='ales.zoulek@gmail.com',
    license='BSD',
    keywords='sentry client standalone'.split(),
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    include_package_data=True,
)


