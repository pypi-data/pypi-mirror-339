from setuptools import setup, find_packages
import pelican_exporter

INSTALL_REQUIRES = [
    "PyYAML~=6.0.1",
    "setuptools~=69.1.1",
    "python-dateutil~=2.9.0.post0",
    "prometheus_client~=0.20.0",
    "dataclasses_json~=0.6.4",
    "requests~=2.31"
]

setup(
    name='pelican_exporter',
    version=pelican_exporter.__version__,
    packages=find_packages(),
    url='https://github.com/scarecr0w12/pelican_exporter',
    license=pelican_exporter.__license__,
    author=pelican_exporter.__author__,
    author_email='jacob@thecorehosting.net',
    description='Metrics exporter for pelican',
    entry_points={
            'console_scripts': [
                'pelican_exporter=pelican_exporter.pelican_exporter:main'
            ]
        },
    python_requires='>=3.11',
    install_requires=INSTALL_REQUIRES
)
