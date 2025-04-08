from setuptools import setup, find_packages

setup(
    name="wiki-mcp",
    version="0.0.1",
    description="A MCP tool for Wikipedia",
    author="hero_system",
    author_email="icraft2170@gmail.com",
    url="https://github.com/The-System-Coperation/mcp-servers/tree/main/wiki-mcp",
    install_requires=[
        "mcp>=1.6.0",
        "beautifulsoup4>=4.12.0",
        "requests",
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wiki-mcp=src.server:run_server',
        ],
    },
    python_requires=">=3.10",
    zip_safe=False,
)
