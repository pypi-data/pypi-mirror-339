from setuptools import setup, find_packages
import pelican_exporter

setup(
    name='pelican_exporter',
    version=pelican_exporter.__version__,
    packages=find_packages(),
    url='https://github.com/scarecr0w12/pelican_exporter',
    license=pelican_exporter.__license__,
    author=pelican_exporter.__author__,
    author_email='jacob@thecorehosting.net',
    description='Metrics exporter for pelican',
    install_requires=open('requirements.txt').readlines(),
    entry_points={
            'console_scripts': [
                'pelican_exporter=pelican_exporter.pelican_exporter:main'
            ]
        }
)
