import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='auth-app',
    package = 'auth_app',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    description='Reusable Authentication APP',
    long_description=README,
    url='https://bitbucket.org/solopt/auth-app/',
    author='Ricardo Lobo',
    author_email='ricardolobo@soloweb.pt',
    install_requires = [
    'django>=1.9.7',
    'djangorestframework>=3.3.3',
    'djangorestframework-jwt>=1.8.0',
    'requests>=2.2.1',
    'PyJWT>=1.4.0,<2.0.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
