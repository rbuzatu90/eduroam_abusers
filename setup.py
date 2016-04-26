import os
import ssl

from setuptools import setup
ssl._create_default_https_context = ssl._create_unverified_context

def read(fname):
    if os.path.exists(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="eduroam_abusers",
    version="0.0.2",
    author="Remus Buzatu",
    author_email="r.buzatu90@gmail.com",
    description="The app can help network administrators to take notice of users that exceed certain amount of network traffic",
    packages=["eduroam_abusers"],
    long_description=read('README.md'),
    entry_points={
        'console_scripts': [
            'abusers = eduroam_abusers.main:main',
        ]
    },
    install_requires=["keyring", "keyrings.alt"],
)
