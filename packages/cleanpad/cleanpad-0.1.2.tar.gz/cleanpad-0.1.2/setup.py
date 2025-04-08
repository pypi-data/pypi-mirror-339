from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cleanpad",
    version="0.1.2",
    author="Omdeep Borkar",
    author_email="omdeeborkar@gmail.com",
    description="Text cleaner and formatter for handling messy copy-pasted content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Omdeepb69/cleanpad",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.6",
    keywords="text cleaning formatting normalization",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/cleanpad/issues",
        "Source": "https://github.com/yourusername/cleanpad",
    },
)