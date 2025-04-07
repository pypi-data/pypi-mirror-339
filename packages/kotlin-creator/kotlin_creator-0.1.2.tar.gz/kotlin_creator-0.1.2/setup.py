from setuptools import setup, find_packages

setup(
    name="kotlin-creator",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
    'console_scripts': [
        'kotlin=kotlin_creator.cli:main',
    ],
},
    author="9tech",
    author_email="your.email@example.com",
    description="A command-line tool for Kotlin project management",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kotlin-cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="kotlin,android,clean-architecture,project-management,cli,development",
)