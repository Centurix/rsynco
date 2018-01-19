from distutils.core import setup  # pragma: no cover


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
    install_requires=[
        "configobj",
        "CherryPy",
        "psutil",
        "jsonschema",
        "schedule"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Archiving :: Backup",
        "Operating System :: POSIX",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Information Technology",
        "Framework :: CherryPy",
    ]
)  # pragma: no cover
