from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_samuell_shoiti",
    version="0.0.1",
    author="Samuell Shoiti",
    author_email="sppaulisto972@gmail.com",
    description="Image Processing package using skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThePersonWhoLikesUndertale/image-processing-package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)