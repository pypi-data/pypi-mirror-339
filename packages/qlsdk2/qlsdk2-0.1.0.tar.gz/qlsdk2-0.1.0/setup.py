# setup.py
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qlsdk2",
    version="0.1.0",
    author="hehuajun",
    author_email="hehuajun@eegion.com",
    description="SDK for quanlan device",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hehuajun/qlsdk",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=open("requirements.txt").read().splitlines(),
    include_package_data=True,
    # entry_points={
    #     'console_scripts': [
    #         'qlsdk-cli=qlsdk.cli:main',  # 如果有命令行工具
    #     ],
    # },
)