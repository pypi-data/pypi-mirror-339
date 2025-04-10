from setuptools import setup, find_packages
try:
    from fdbtk_utils.const._version import __name__, __version__
except Exception as e:
    __name__ = 'fdbtk-utils'
    __version__ = '0.0.4'

long_description = """
fdbtk-utils is a Python utility package designed to streamline the automation of 
infrastructure provisioning, virtual machine (VM) configuration, and system-level 
testing for Foundation Database environments. Built with cloud-native principles 
in mind, this toolkit enables teams to rapidly and reliably manage their infrastructure 
lifecycle and validate deployments in dynamic environments.
"""

setup(
    name=__name__,
    version=__version__,
    packages=find_packages(),
    description=__name__,
    long_description_content_type='text/plain',
    long_description=long_description,
    url='https://github.com/FoundationDB/fdb-joshua',
    download_url='https://github.com/FoundationDB/fdb-joshua',
    project_urls={
        'Documentation': 'https://github.com/FoundationDB/fdb-joshua'},
    author='Baxter Rogers',
    author_email='baxpr@vu1.org',
    python_requires='>=3.11',
    platforms=['Linux'],
    license='GNU',

)
