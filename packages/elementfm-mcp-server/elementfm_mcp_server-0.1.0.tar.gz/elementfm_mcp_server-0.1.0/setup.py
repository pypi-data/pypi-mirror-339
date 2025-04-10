from setuptools import setup, find_packages

setup(
    name="elementfm-mcp-server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastmcp",
        "pydantic",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'elementfm-mcp=elementfm_mcp_server.server:main',
        ],
    },
    author="Element.fm",
    description="MCP server for Element.fm",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/elementfm/elementfm-mcp-server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
) 