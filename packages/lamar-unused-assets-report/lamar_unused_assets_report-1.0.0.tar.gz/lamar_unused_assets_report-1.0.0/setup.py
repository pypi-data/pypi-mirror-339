from setuptools import setup, find_packages

setup(
    name="lamar-unused-assets-report",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "lamar-unused-assets-report = lamar_unused_assets_report.main:main"
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Generate a CSV report for unused CMS assets from Lamar's API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lamar-unused-assets-report",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)
