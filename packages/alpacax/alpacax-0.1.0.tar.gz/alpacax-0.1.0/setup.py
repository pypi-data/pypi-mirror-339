from setuptools import setup, find_packages
import os

setup(
    name="alpacax",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "transformers>=4.36.2",
        "peft>=0.9.0",
        "accelerate>=0.27.2",
        "bitsandbytes>=0.42.0",
        "torch>=2.1.0"
    ],
    entry_points={
        "console_scripts": [
            "alpacax=alpacax.cli:run_chat"
        ]
    },
    include_package_data=True,
    description="LoRA-powered GPT2 AlpacaX CLI",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Sully Greene",
    url="https://github.com/SullyGreene/AlpacaX",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.8",
)
