from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="risk-assessment",
    version="1.0.0",
    author="LT",
    author_email="your.email@example.com",
    description="A comprehensive enterprise risk assessment system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/enterprise-risk-assessment",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "openpyxl>=3.0.0",
        "PyYAML>=5.4.0",
    ],
    entry_points={
        "console_scripts": [
            "risk-assessment=risk_assessment_package:assess_risk",
        ],
    },
    package_data={
        "": ["*.yaml"],
    },
    include_package_data=True,
) 