from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="vdraw",
    version="0.1.3",
    description="A library for working with segmentation masks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="workerlv",
    url="https://github.com/workerlv/vdraw",
    project_urls={"Documentation": "https://vdraw-doc.streamlit.app/"},
    packages=find_packages(),
    install_requires=["numpy", "opencv-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
