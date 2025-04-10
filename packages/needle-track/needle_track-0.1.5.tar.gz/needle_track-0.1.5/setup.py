from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="needle-track",
    version="0.1.5",
    author="Xinyue Sheng",
    author_email="XinyueSheng@outlook.com",
    description="Transient Recognition, Annotation, and Classification Kit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XinyueSheng2019/NEEDLE-TRACK",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    python_requires=">=3.11",
    entry_points={
        'console_scripts': [
            'needle-track=needle_track.__main__:main',
        ],
    },
    install_requires=[
        'numpy>=2.0.0',
        'pandas>=2.0.0',
        'astropy>=7.0.0',
        'lasair>=0.1.1',
        'requests>=2.30.0',
    ],
    project_urls={
        "Bug Reports": "https://github.com/XinyueSheng2019/NEEDLE-TRACK/issues",
        "Source": "https://github.com/XinyueSheng2019/NEEDLE-TRACK",
    },
) 