from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in humman_resource/__init__.py
from humman_resource import __version__ as version

setup(
	name="humman_resource",
	version=version,
	description="humman resource application",
	author="ahmed",
	author_email="a.a.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
