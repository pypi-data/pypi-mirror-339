from setuptools import setup, find_packages

setup(
    name="D8N8D",
    version="1.0.0",
    description="An unstoppable exit method for Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Shridhar",
    author_email="shridhuu166@gmail.com",
    url="https://github.com/shridhuu",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
