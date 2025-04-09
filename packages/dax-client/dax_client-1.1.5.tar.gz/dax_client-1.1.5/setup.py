from setuptools import setup, find_packages
try:
    from dax_client.const._version import __name__, __version__
except Exception as e:
    __name__ = 'dax-client'
    __version__ = '1.1.5'

long_description = """
XNAT is a flexible imaging informatics software platform for organizing and managing 
imaging data. DAX is a Python project that provides a uniform interface to run 
pipelines on a cluster by pulling data from an XNAT database via REST API calls. 
The dax client further enhances DAX by offering powerful command-line tools that 
streamline extracting information from XNAT, creating pipelines (spiders/processors), 
building projects on XNAT with pipeline assessors, managing pipeline execution on a cluster, 
and automatically uploading results back to XNAT. By leveraging XnatUtils commands, 
the dax client also enables a programmatic workflow for interacting directly with XNAT in Python.  
"""

setup(
    name=__name__,
    version=__version__,
    packages=find_packages(),
    description=__name__,
    long_description_content_type='text/plain',
    long_description=long_description,
    url='https://github.com/VUIIS/dax_bids',
    download_url='https://github.com/VUIIS/dax_bids',
    project_urls={
        'Documentation': 'https://github.com/VUIIS/dax_bids'},
    author='Baxter Rogers',
    author_email='baxpr@vu1.org',
    python_requires='>=3.6',
    platforms=['MacOS', 'Linux'],
    license='MIT',

)
