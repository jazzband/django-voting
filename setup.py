from setuptools import setup, find_packages


setup(
    name='django-voting',
    use_scm_version=True,
    description='Generic voting application for Django',
    author='Jonathan Buchanan',
    author_email='jonathan.buchanan@gmail.com',
    maintainer='Jannis Leidel',
    maintainer_email='jannis@leidel.info',
    url='https://github.com/pjdelport/django-voting',

    package_dir = {'':'src'},
    packages=find_packages('src'),

    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=[
        'Django >=1.4, <1.9',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
