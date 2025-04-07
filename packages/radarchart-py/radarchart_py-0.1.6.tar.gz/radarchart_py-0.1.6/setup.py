from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="radarchart-py",
    version="0.1.6",
    author="Sabir Ribas",
    author_email="sabirribas+pypi@gmail.com",
    description="RadarChart: A Python library for customizable radar charts (spider plots)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sabirribas/radarchart",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=install_requires,  # Load dependencies from file
    entry_points={
        'console_scripts': [
            'radarchart=radarchart.main:main',  # Example CLI entry point
        ],
    },
    include_package_data=True,
)
