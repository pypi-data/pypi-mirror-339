from setuptools import setup, find_packages

setup(
    name="folder-structure-tool",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'PeekDir = PeekDir.cli:main'
        ],
    },
    install_requires=[],
    author="Ayyuce Demirbas",
    author_email="a.ayyuced@gmail.com",
    description="Prints folder structure with smart file truncation",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ayyucedemirbas/PeekDirl",
    license="GPL-3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)