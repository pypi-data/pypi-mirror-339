from setuptools import setup, find_packages

setup(
    name='WebScraperX',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests', 'beautifulsoup4'],
    author='Ruzgar',
    description='Bir web sitesini alir ve HTML yapisini Python objesi olarak dondurur.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ruzgar/WebScraperX',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.6',
)
