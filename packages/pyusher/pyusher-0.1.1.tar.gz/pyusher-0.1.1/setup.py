from setuptools import setup, find_packages

setup(
    name="pyusher",
    version="0.1.1",
    packages=find_packages(),  # This will include the package directory named agent_server
    install_requires=[
        "fastapi",
        "structlog",
        "uvicorn"
    ]
)
