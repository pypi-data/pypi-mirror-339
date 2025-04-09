
from setuptools import setup, find_packages

setup(
    name="orange-mcp-server-make",
    version="0.3.1",
    description="A Model Context Protocol server providing access to make functionality",
    author="orange",
    author_email="mseep@example.com",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp>=1.0.0', 'pydantic>=2.0.0'],
    keywords=["orange"] + ['make', 'mcp', 'llm', 'automation'],
)
