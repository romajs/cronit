# http://click.pocoo.org/5/setuptools/#setuptools-integration

from setuptools import setup, find_packages

setup(
	name='cronit',
	version='0.1',
	py_modules=['cronit'],
	packages=find_packages(),
	include_package_data=True,
	install_requires=[
		'Click',
	],
	entry_points='''
		[console_scripts]
		cronit=cronit:cli
	''',
)