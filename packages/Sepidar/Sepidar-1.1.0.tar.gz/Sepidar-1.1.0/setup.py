from setuptools import setup, find_packages

def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()

setup(
    name='Sepidar',
    version='1.1.0',
    author='Mahdi Ahmadi',
    author_email='mahdiahmadi.1208@gmail.com',
    description='An asynchronous Python wrapper for the Sepidar API Search.',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://api-free.ir',
    license='MIT',

    packages=find_packages(),
    include_package_data=True,

    install_requires=[ 
        'aiohttp>=3.8.1',
    ],

    extras_require={
        'dev': ['pytest', 'black', 'flake8'],
        'docs': ['mkdocs', 'pdoc3'],
    },

    entry_points={
        'console_scripts': [
            'eitaapy-cli=eitaapy.cli:main',
        ],
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Environment :: Console',
        'Natural Language :: English',
    ],

    python_requires='>=3.6', 

    keywords='Sepidar, bot, Google, python, asynchronous, aiohttp', 

    project_urls={
        'Bug Tracker': 'https://t.me/dev_jav',
        'Documentation': 'https://api-free.ir/',
        'Source Code': 'https://api-free.ir/',
    },
)
