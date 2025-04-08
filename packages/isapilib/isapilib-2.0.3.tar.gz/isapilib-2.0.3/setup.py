from setuptools import setup, find_packages

setup(
    name='isapilib',
    version='2.0.3',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'templates': ['templates/*'],
        'static': ['static/*'],
    },
    install_requires=[
        'django>=4.2',
        'djangorestframework>=3.0.0',
        'djangorestframework-simplejwt>=5.0.0',
    ],
)
