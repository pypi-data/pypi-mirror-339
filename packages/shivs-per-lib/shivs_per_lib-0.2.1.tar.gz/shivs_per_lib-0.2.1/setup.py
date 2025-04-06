from setuptools import setup, find_packages

setup(
    name='shivs_per_lib',
    version='0.2.1',
    packages=find_packages(),
    description='A personal utility package by Shivsamb Harkare.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Shivsamb Mangalkumar Harkare',
    author_email='shivsamb1984@gmail.com',
    url='https://github.com/yourusername/shivs_per_lib',  # Replace if available
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[],  # Add dependencies here
    python_requires='>=3.6',
)
