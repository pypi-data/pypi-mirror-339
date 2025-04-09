from setuptools import setup, find_packages

setup(
    name="py-shopify-graphql",
    version="0.1.0",
    description="A Python client for making Shopify GraphQL API requests",
    author="Pawan More",
    author_email="hello@pawanmore.com",
    url="https://github.com/pawan1793/py-shopify-graphql-client",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)