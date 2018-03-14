# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    # packages     = find_packages(include=['bs4']),
    entry_points = {'scrapy': ['settings = gsites.settings']},
)
