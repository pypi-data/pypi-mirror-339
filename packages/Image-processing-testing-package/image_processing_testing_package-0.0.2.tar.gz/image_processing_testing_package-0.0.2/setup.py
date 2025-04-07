from setuptools import setup, find_packages

with open("README.md", "r") as f:
  page_description = f.read()

with open("requirements.txt", "r") as f:
  required = f.read().splitlines()
  
setup(
  name="Image_processing_testing_package",
  version="0.0.2",
  author="Leonardo Vieira Moreira",
  author_email="lvm9508@gmail.com",
  description="image processing package",
  long_description=page_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Le0Vieir4/image-processing-package",
  packages=find_packages(),
  install_requires=required,
  python_requires=">=3.8"
)