from setuptools import setup, find_packages
try:
    from deployment_info.static._info import __name__, __version__
except Exception as e:
    __name__ = 'deployment-info'
    __version__ = '1.2.6'


setup(
    name=__name__,
    version=__version__,
    packages=find_packages(),
    description=__name__,
    long_description_content_type='text/plain',
    long_description='This Python library provides a simple interface for retreiving the system deployment information.',
    url='https://github.com/pbullian/k8s_deployments_info',
    download_url='https://github.com/pbullian/k8s_deployments_info',
    project_urls={
        'Documentation': 'https://github.com/pbullian/k8s_deployments_info'},
    author='Tom Christian',
    author_email='tom.christian@openxta.com',
)
