from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Other Audience',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='TriangleDetective',
    version='0.0.1',
    description="Triangular Trigonometry",
    long_description_content_type='text/plain',
    long_description=open('README.txt').read() + '\n\n' + open("CHANGELOG.txt").read(),
    url='',
    author="Abhinav S Nair",
    author_email="svnair.1984@gmail.com",
    license='MIT',
    classifiers=classifiers,
    keywords='trigonometry',
    packages=find_packages(),
    install_requires=[''],
project_urls={ 'Documentation': 'https://PyTrigPyCharm.readthedocs.io', 'Source': 'https://github.com/Sarish002/PyTrigPyCharm', 'Bug Tracker': 'https://github.com/Sarish002/PyTrigPyCharm/issues', }
)
