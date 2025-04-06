from setuptools import setup, find_packages

setup(
    name="utils-me",
    version="0.1.3.10",
    author="Siguifowa Yeo",
    author_email="siguifowa.yeo@gmail.com",
    package_dir={"": "source"},
    packages=find_packages(where="source"),
    description="This a sort description",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SiguiNag/UtilsMe.git",
        classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    python_requires='>=3.7',
    install_requires=[
        'pandas', 
        'requests',
        'pydantic',
        'pyyaml'
    ],
)