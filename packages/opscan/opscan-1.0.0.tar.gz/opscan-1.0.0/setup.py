from setuptools import setup, find_packages

setup(
    name="opscan",
    version="1.0.0",
    description="A fast and simple Python-based open port scanner.",
    author="Mr.Balakavi",
    author_email="balakavi64@gmail.com",
    url="https://github.com/yourusername/opscan",  # Optional, update if needed
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "opscan=opscan.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Utilities",
        "Intended Audience :: Developers"
    ],
    python_requires='>=3.6',
    license="MIT",
    include_package_data=True,
)
