from setuptools import setup, find_packages

setup(
    name='sybsc',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'sybsc': ['data.txt']},
    description='A simple package to retrieve your custom text anywhere.',
    author='Detective',
    author_email='codedbybipin28@outlook.com',
    url='https://github.com/bipinyada28/sybsc',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)

