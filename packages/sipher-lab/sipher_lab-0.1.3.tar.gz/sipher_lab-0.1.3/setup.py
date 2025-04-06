from setuptools import setup, find_packages

setup(
    name="sipher-lab",
    version="0.1.3",  # Incremented version
    packages=find_packages(),
    package_data={
        'sipher_package': ['cipher_code/*/*.py'],
    },
    entry_points={
        'console_scripts': [
            'get_siphers=sipher_package.cli:main',
        ],
    },
    install_requires=[
        'setuptools>=68.0.0',
    ],
    author="Captain",  # Add your actual name
    author_email="your.email@example.com",  # Add your email
    description="Classic cipher implementations including Vernam cipher",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sipher-lab",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="ciphers cryptography vernam encryption",
    license="MIT",
    platforms=["any"],
)