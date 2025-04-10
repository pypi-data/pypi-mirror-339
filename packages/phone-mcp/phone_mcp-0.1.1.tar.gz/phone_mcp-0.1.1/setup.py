from setuptools import setup, find_packages

setup(
    name="phone-mcp",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.6.0",
        "aiohttp>=3.8.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A phone control MCP plugin using ADB",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/phone-mcp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "mcp.plugins": [
            "phone=phone.phone_mcp:mcp"
        ]
    }
)
