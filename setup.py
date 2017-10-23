from distutils.core import setup

setup(
    name='rsynco',
    version='0.1dev',
    author='Chris Read',
    author_email='centurix@gmail.com',
    packages=['rsynco'],
    license='BSD',
    long_description=open('README.md').read(),
    keywords="rsync cherrypy rest api",
    url="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Archiving :: Backup",
        "Operating System :: POSIX",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Information Technology",
        "Framework :: CherryPy",
    ]
)
