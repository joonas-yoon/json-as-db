import setuptools

setuptools.setup(
    name='json-db',
    version='0.0.1.dev0',
    license='MIT',
    author='joonas',
    author_email='joonas.yoon@gmail.com',
    description='Using JSON as very lightweight database',
    long_description=open('README.md', encoding='utf-8').read(),
    url='https://github.com/joonas-yoon/json-db',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: System :: Filesystems',
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    keywords=['json', 'lightweight', 'database'],
    python_requires='>=3.6.0',
)
