# setup.py
from setuptools import setup, find_packages

setup(
    name="sardugame",  # Nome del pacchetto
    version="0.4.1",  # Versione del pacchetto
    packages=find_packages(),  # Trova tutte le cartelle con __init__.py
    install_requires=[
        "pygame",  # Aggiungi qui le dipendenze (in questo caso tkinter per la GUI)
    ],
    author="Giovanni",
    author_email="cetriolonazionale@gmail.com",
    description="un motore per crare giochi 2d",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/giovanni/sardugame",  # Modifica con il tuo URL GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
