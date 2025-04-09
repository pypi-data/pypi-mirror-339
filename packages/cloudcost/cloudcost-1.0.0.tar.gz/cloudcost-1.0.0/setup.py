from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="cloudcost",
    version="1.0.0",
    packages=find_packages(),  # Find all obfuscated packages
    include_package_data=True,  # Include all packaged files
    install_requires=[
        "boto3>=1.20.0",
        "colorama>=0.4.4",
        "tabulate>=0.8.9",
        "botocore~=1.37.13",
        "setuptools~=70.0.0",
        "requests~=2.32.3",
        "sentry-sdk~=2.24.0"
    ],
    entry_points={
        "console_scripts": [
            "cloudcost=cloud_cost_optimizer.cli:main",
        ],
    },
    author="Kaushal",
    author_email="kaushal@auron.cloud",
    description="Cloud Cost Optimization Tool",
    keywords="aws, cost, optimization, cloud",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Proprietary",
    license_files=["LICENSE"],
    project_urls={
        "Home page": "https://auron.cloud",
        "Bug Reports": "https://github.com/AuronCloud/cloudcost/issues",
        "Source": "https://github.com/AuronCloud/cloudcost/",
        "Documentation": "https://github.com/AuronCloud/cloudcost/blob/main/README.md",
        "Donate": "https://github.com/sponsors/kaushal540",
    }
)
