from setuptools import setup, find_packages

setup(
    name='blueprint',
    version='0.1',
    description='Test my api',
    long_description="",
    author='Sourcepirate',
    author_email='plasmashadowx@gmail.com',
    url='https://github.com/sourcepirate/blueprint',
    license="",
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=[
        "requests",
        "jsonschema"
    ],
    test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console'],
    scripts=['bin/blueprint']
)