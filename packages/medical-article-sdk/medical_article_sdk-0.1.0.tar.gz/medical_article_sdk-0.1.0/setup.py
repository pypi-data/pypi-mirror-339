from setuptools import setup, find_packages
import os

# 递归查找所有 .pyc 文件
def find_pyc_files(package_dir):
    pyc_files = []
    for root, _, files in os.walk(package_dir):
        for file in files:
            if file.endswith(".pyc"):
                pyc_files.append(os.path.relpath(os.path.join(root, file), package_dir))
    return pyc_files

# 获取所有 .pyc 文件
package_dir = "medical_article_sdk"
pyc_files = find_pyc_files(package_dir)

# 递归排除所有 .py 文件
def exclude_py_files(package_dir):
    py_files = []
    for root, _, files in os.walk(package_dir):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.relpath(os.path.join(root, file), package_dir))
    return py_files

py_files = exclude_py_files(package_dir)

setup(
    name="medical_article_sdk",
    version="0.1.0",
    author="imuzhangy",
    author_email="imuzhangying@gmail.com",
    description="A package for correcting medical subtitles",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=py_files),  # 排除 .py 文件
    include_package_data=True,
    package_data={
        'medical_article_sdk': ['config.json', 'medical_prompt.txt', 'title_note_prompt.txt'] + pyc_files,
    },
    install_requires=[
        'requests',
        'python-docx',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)