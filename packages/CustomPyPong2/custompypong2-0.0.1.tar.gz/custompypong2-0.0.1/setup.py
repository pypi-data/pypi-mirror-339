from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: End Users/Desktop',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='CustomPyPong2',
    version='0.0.1',
    description="Ping Pong package",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read() + '\n\n' + open("CHANGELOG.txt").read(),
    url='',
    author="Abhinav S Nair",
    author_email="svnair.1984@gmail.com",
    license='MIT',
    classifiers=classifiers,
    keywords='Table Tennis',
    packages=find_packages(),
    install_requires=['Pygame'],
    project_urls={'Documentation': 'https://CustomPyPong2.readthedocs.io',
                   'Source': 'https://github.com/Sarish002/CustomPyPong2',
                   'Bug Tracker': 'https://github.com/Sarish002/CustomPyPong2/issues'}
)
