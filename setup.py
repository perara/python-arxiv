from setuptools import setup

setup(
    name="python-arxiv",
    version="1.0.0",
    packages=["arxiv"],
    install_requires=[
        'feedparser',
    ],
    author="Per-Arne Andersen",
    author_email="per@sysx.no",
    description="Python wrapper for the arXiv API.",
    license="MIT",
    keywords="arxiv wrapper papers",
    url="https://github.com/perara/python-arxiv",
    download_url="https://github.com/perara/python-arxiv/tarball/1.0.0",
)
