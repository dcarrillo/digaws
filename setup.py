from digaws import __description__, __version__

from setuptools import setup


def get_long_description() -> str:
    with open('README.md', 'r', encoding='utf-8') as fh:
        return fh.read()


setup(
    name='digaws',
    version=__version__,
    description=__description__,
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='http://github.com/dcarrillo/digaws',
    author='Daniel Carrillo',
    author_email='daniel.carrillo@gmail.com',
    license='Apache Software License',
    packages=['digaws'],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['digaws=digaws.digaws:main']
    },
    install_requires=[
          'python-dateutil~=2.8',
          'requests~=2.25',
    ]
)
