from setuptools import setup, find_packages

setup(
    name="gitbase",
    version="0.5.6",
    author="Taireru LLC",
    author_email="tairerullc@gmail.com",
    description="A GitHub-based database system ('GitBase') offering offline backups and optional encryption.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TaireruLLC/gitbase",
    packages=find_packages(),
    install_requires=[
        "requests",
        "cryptography",
        "altcolor>=0.0.5",
        "moviepy",
        "fancyutil==0.0.3",
        "numpy",
        "opencv-python",
        "pyaudio",
        "wave"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
)
