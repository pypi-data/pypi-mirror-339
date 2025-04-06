from setuptools import setup, find_packages

setup(
    name='awholenewworld',  # Your package name
    version='0.1.2',  # Version of the library
    author='Agamjot',
    author_email='agamjotlamba55@gmail.com',
    description='A collection of Python packages for various utilities and functionalities.',
    long_description=open('README.md', encoding='utf-8').read(),  # Readme with utf-8 encoding
    long_description_content_type='text/markdown',  # Markdown file format
    packages=find_packages(),  # Automatically include all Python packages in the folder
    classifiers=[
        'Programming Language :: Python :: 3',  # Python 3 support
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',  # Platform-independent
    ],
    python_requires='>=3.6',  # Minimum Python version required
    install_requires=[  # External dependencies
        'cohere',  # Add any other dependencies here
    ],
)
