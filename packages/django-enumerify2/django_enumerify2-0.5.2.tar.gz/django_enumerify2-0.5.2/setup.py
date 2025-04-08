# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-enumerify2',
    version='0.5.2',
    author=u'Faisal Mahmud',
    author_email='faisal@willandskill.se',
    packages=find_packages(),
    url='http://github.com/willandskill/django-enumerify2',
    license='BSD licence, see LICENCE.txt',
    description='Simple Enums for Django when working with choices in model fields.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    test_suite="testproject.runtests.runtests",
)