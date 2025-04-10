from setuptools import setup, find_packages

setup(
    name="mcp-coze-server",
    version="0.1.12",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "cozepy-flink",
        "mcp>=1.6.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.11",
) 