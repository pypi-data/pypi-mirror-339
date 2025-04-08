from setuptools import setup, find_packages

setup(
    name="vbi-evaluate",  # tên sẽ hiển thị trên PyPI
    version="0.1.0",
    author="LeeMinHoon",
    author_email="your_email@example.com",
    description="A package for evaluating and fact-checking documents.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vbi-evaluate",  # nếu có
    packages=find_packages(),  # tự động tìm package (như "package/")
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
