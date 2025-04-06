from setuptools import find_packages, setup
import os

# 
readme_path = "README.md"
long_description = open(readme_path).read() if os.path.exists(readme_path) else ""

setup(
    name="easyxp",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "numpy",
    ],
    python_requires=">=3.6",  # 指定最低 Python 版本
    author="Xianpu JI",
    author_email="xianpuji@hhu.edu.cn",
    description="Simple add quiver legend toolkit for matplotlib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Blissful-Jasper/Easyxp",
    classifiers=[
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,  
    license="MIT",
    keywords="quiver legend matplotlib",
)
