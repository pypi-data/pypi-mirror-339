from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
  name="blame-g",
  version="0.0.0",
  author="Mohammed Muzammil Anwar",
  author_email="mohammad.muzammil100@gmail.com",
  description="",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="",
  packages=find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.7",
  install_requires=[
    "argparse",
    "gitpython",
    "rich",
  ],
  entry_points={
    "console_scripts": [
      "blame-g=blame_g.main:main",
    ],
  },
)
