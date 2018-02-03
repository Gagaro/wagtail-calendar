from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='wagtail-calendar',
    version='1.0.1',
    description='A planning calendar for wagtail',
    long_description=readme(),
    url='https://github.com/Gagaro/wagtail-calendar',
    author='Gagaro',
    author_email='gagaro42@gmail.com',
    license='BSD3',
    packages=['wagtail_calendar'],
    install_requires=[
    ],
    zip_safe=False,
    include_package_data=True,
)