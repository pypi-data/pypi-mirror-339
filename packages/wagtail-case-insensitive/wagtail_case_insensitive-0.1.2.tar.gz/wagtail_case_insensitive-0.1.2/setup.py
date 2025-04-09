from setuptools import setup, find_packages
from os.path import abspath, dirname, join
from case_insensitive import __version__


path = abspath(dirname(__file__))
with open(join(path, "README.rst")) as f:
    readme = f.read()

setup(
    name="wagtail-case-insensitive",
    version=__version__,
    description="Fixes case errors in URLs by redirecting.",
    url="https://github.com/FullFact/wagtail-case-insensitive",
    author="Andy Lulham",
    author_email="andy.lulham@fullfact.org",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        'wagtail>=6.4',
    ],
    long_description=readme,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.12',
        'Framework :: Django',
        'Framework :: Django :: 5.1',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
