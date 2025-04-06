from setuptools import setup, find_packages

setup(
    name="at-client-workflow",
    version="0.1.1",
    description="AT Client and Schema Package for AT Workflow API",
    author="Ray",
    author_email="rayanywhere@gmail.com",
    url="https://github.com/apex-trader/at-backend-workflow",
    packages=find_packages(include=['at_client_workflow', 'at_client_workflow.*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=1.8.0",
    ],
) 