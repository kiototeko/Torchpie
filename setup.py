import io
import os
import re

from setuptools import find_packages, setup


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def find_requirements(file_path):
    install_requires = []
    dependency_links = []

    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line.startswith('-e'):
                dependency_links.append(line[3:])
            else:
                install_requires.append(line)

    return install_requires, dependency_links


VERSION = find_version('torchpie', '__init__.py')

install_requires, dependency_links = find_requirements('requirements.txt')


setup(
    name='torchpie',
    version=VERSION,
    description='Pytorch utils',
    author='SunDoge',
    packages=find_packages(exclude=('test',)),
    install_requires=install_requires,
    dependency_links=dependency_links,
)
