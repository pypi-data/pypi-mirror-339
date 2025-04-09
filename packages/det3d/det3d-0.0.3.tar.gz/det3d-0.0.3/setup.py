from setuptools import setup, find_packages

with open("readme.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "torch==1.8.0",
    'numpy==1.19.2',
    ] 

setup(
    name="det3d",
    version="0.0.3",
    author="Tao Xiang",
    author_email="xiang.tao@outlook.de",
    description="A package of 3D object detection models",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/leoxiang66/3D-Detection",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
    ],
)