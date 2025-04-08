from setuptools import setup, find_packages
from pathlib import Path

# Direktori proyek
this_dir = Path(__file__).parent
readme_path = this_dir / "README.md"

setup(
    name="pinequiz",
    version="1.0.4",
    author="openpineaplehub",
    author_email="openpineaple@gmail.com",
    description="🍍 PineQuiz CLI - Jalankan kuis terenkripsi dari GitHub",
    long_description=readme_path.read_text(encoding="utf-8") if readme_path.exists() else "🍍 PineQuiz CLI - Jalankan kuis terenkripsi dari GitHub.",
    long_description_content_type="text/markdown",
    url="https://github.com/openpineapletools/pinequiz",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pinequiz = pinequiz.pinequiz:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="cli quiz github kuis terminal encrypted",
    python_requires=">=3.6",
    install_requires=[
        "requests",
    ],
    project_urls={
        "Source": "https://github.com/openpineapletools/pinequiz",
        "Bug Tracker": "https://github.com/openpineapletools/pinequiz/issues",
    },
    license="MIT",
    zip_safe=False,
)
