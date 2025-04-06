from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='EduTri',
    version='0.0.1',
    description="Trigonometry package",
    long_description_content_type='text/plain',
    long_description=open('README.txt').read() + '\n\n' + open("CHANGELOG.txt").read(),
    url='',
    author="Abhinav S Nair",
    author_email="svnair.1984@gmail.com",
    license='MIT',
    classifiers=classifiers,
    keywords='Education',
    packages=find_packages(),
    install_requires=[''],
    project_urls={ 'Documentation': 'https://EduTri.readthedocs.io', 'Source': 'https://github.com/Sarish002/EduTri', 'Bug Tracker': 'https://github.com/Sarish002/EduTri/issues', }
)
