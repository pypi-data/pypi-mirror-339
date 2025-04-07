from setuptools import setup, find_namespace_packages

setup(
    name="basalam.backbone-api",
    author="Mohammad Asghari",
    author_email="mhmdasghari1@gmail.com",
    description="Python OpenApi Utilities for FastAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/basalam/backbone-api",
    packages=find_namespace_packages(where='src',
                                     include=['basalam.backbone_api',
                                              'basalam.backbone_api.responses',
                                              'basalam.backbone_api.exceptions',
                                              'basalam.backbone_api.responses.*',
                                              'basalam.backbone_api.exceptions.*',]),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setuptools_git_versioning={"enabled": True},
    setup_requires=["setuptools-git-versioning"],
    install_requires=[
        "pydantic>=2.9.1",
        "fastapi>=0.114.0"
    ]
)
