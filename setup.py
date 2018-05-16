from setuptools import find_packages, setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='wagtail-calendar',
    version='1.0.3',
    description='A planning calendar for wagtail',
    long_description=readme(),
    url='https://github.com/Gagaro/wagtail-calendar',
    author='Gagaro',
    author_email='gagaro42@gmail.com',
    license='BSD3',
    packages=find_packages(),
    install_requires=[
    ],
    zip_safe=False,
    include_package_data=True,
)