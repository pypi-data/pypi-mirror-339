from setuptools import setup, find_packages

setup(
    name='zenquotespy',
    version='0.2.1',
    description='ZenquotesPy is a lightweight Python package that provides easy access to motivational and inspirational quotes from the ZenQuotes.io API.',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='Nilay Sarma',
    packages=find_packages(),
    install_requires=['requests==2.32.3'],
    license="MIT",
    url="https://zenquotespy.pages.dev",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Documentation": "https://zenquotespy.pages.dev",
        "Repository": "https://github.com/nilaysarma/zenquotespy",
        "Release Notes": "https://github.com/nilaysarma/zenquotespy/releases/latest",
    }
)