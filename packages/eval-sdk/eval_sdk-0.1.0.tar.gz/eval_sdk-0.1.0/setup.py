from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eval_sdk",
    version="0.1.0",
    author="jack",
    author_email="your.email@example.com",
    description="A Python SDK for ...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your_sdk",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
        # 其他依赖
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="sdk api client",
)