# setup.py

from setuptools import setup, find_packages

setup(
        name="worldapi",
    version="0.1.0",
    author="EngeenerWerch",
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    description='interacte with world',
    author_email='cyberpony_x@mail.ru',
    url='https://github.com/engineering-wrench/WorldAPI'  # Укажите ссылку на репозиторий
)