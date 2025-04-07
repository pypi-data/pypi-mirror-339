import os
from setuptools import setup, find_packages

# Read long description from README.md
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name='structinit',  # Updated name
    version='1.0.1',
    author='Srijan',
    author_email='srijanbahal.work@example.com',
    description='🛠️ Generate full project structures from markdown blueprints.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/srijanbahal/Projinit',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'structinit=projinit.main:main'  # Updated CLI command
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT",
    keywords=['project scaffolding', 'markdown', 'CLI', 'automation'],
)
