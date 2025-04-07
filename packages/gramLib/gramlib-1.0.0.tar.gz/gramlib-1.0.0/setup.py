import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gramLib", # Измените на желаемое имя (должно быть уникальным на PyPI)
    version="1.0.0",      # Начальная версия
    author="NEFOR",
    author_email="gram@gmail.com",
    description="libraly in create database in gram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/my_gram_library", # Ссылка на репозиторий
    packages=setuptools.find_packages(),  # Автоматически находит пакеты
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', # Минимальная версия Python
)
