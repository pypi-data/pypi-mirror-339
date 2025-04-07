from setuptools import setup, find_packages

setup(
    name='zipit-cli',
    version='1.0.0a1',
    description='A smart zip tool that respects .gitignore and custom patterns',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Zubin James',
    author_email='zubinj.palit2002@gmail.com',  # change this!
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'zipit=zipit.cli:run'
        ]
    },
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
)
