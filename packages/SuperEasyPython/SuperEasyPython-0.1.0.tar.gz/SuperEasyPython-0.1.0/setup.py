from setuptools import setup, find_packages
from setuptools import setup, find_packages

setup(
    name="SuperEasyPython",          # Название на PyPI (должно быть уникальным!)
    version="0.1.0",             # Версия (семантическое версионирование)
    packages=find_packages(),    # Автоматически находит все пакеты
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "aiogram>=2.23.1",
        "tqdm>=4.60.0",
        "PySide6>=6.4.0"
    ],         # Зависимости (например, ["requests>=2.25.1"])
    author="RedFlyMeer",
    author_email="redflymeer@gmail.com",
    description="EasyPython",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/redflymeer/SuperEasyPython",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",     # Минимальная версия Python
)
