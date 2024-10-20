import os
from setuptools import setup, find_packages

setup(
    name='job-app-helper',
    version='0.1.0',
    url='https://github.com/bglid/job-application-helper',
    author='Benjamin Glidden',
    author_email='benjamin.h.glidden@gmail.com',
    description='Web Scraper + NLP pipeline to help with job applications',
    # long_description=open(os.path.join()
    license="MIT",
    packages=find_packages(where='src'),
    package_dir={"": 'src'},
    install_requires=[
        'streamlit',
        'beautifulsoup4',
        'requests',
        'spacy', 
        'python-docx',
        'pytextrank'
    ],
    python_requires = '>=3.7.0'
)