from setuptools import setup, find_packages

setup(
    name='api_investment_risk',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=2.2.3",
        "requests>=2.32.3",
        "numpy>=2.2.3"
    ]
        
)