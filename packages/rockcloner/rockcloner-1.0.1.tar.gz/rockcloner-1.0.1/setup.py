from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rockcloner",
    version="1.0.1",
    author="Devrock",
    author_email="audriajou81@gmail.com",
    description="Discord Server Cloning Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/browished/rock-clonerv1",
    packages=find_packages(),
    install_requires=[
        'discord.py-self>=1.9.0',
        'inquirer>=2.10.1',
        'colorama>=0.4.4',
        'rich>=12.5.1',
        'pyfiglet>=0.8.post1',
        'aiohttp>=3.8.1',
        'psutil>=5.9.0',
        'pypresence>=4.2.0',
        'questionary>=1.10.0',
        'requests>=2.28.1',
        'readchar>=3.0.5',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'rockcloner=rockcloner.cli:run',
        ],
    },
)