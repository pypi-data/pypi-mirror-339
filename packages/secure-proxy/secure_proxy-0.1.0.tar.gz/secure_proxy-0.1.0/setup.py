from setuptools import setup, find_packages

setup(
    name="secure_proxy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
    ],
    author="Abduvohid",
    author_email="abdujalilov2629@gmail.com",
    description="Maxfiy proxy orqali so‘rov yuborish uchun kutubxona",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abduvohid26/secure_proxy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
