from setuptools import setup, find_packages

setup(
    name='pychunk',
    version='0.1',
    packages=find_packages(include=['pychunk']),
    scripts=['scripts/python-scripts/classify-python-code.sh', 
             'scripts/python-scripts/find-node-relationships.sh', 
             'scripts/python-scripts/generate-node-metadata.sh'],
    author="Jaime Sancho Molero", 
    author_email="jimysanchomolero@gmail.com", 
)
