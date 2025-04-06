# setup.py
from setuptools import setup, find_packages
import os

# Read the contents of README file
base_dir = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "TrainSense: An enhanced toolkit for deep learning model analysis, profiling, and training optimization."


setup(
    name="TrainSense",
    version="0.1.0",
    packages=find_packages(exclude=["exemples", "tests*", "*.tests", "*.tests.*", "tests"]), # Exclusion plus robuste
    # Lister directement les dépendances ici:
    install_requires=[
        'psutil>=5.8.0',
        'torch>=1.8.0', # Garder une version minimale raisonnable
        'GPUtil>=1.4.0'
        # Ajouter d'autres dépendances directes si nécessaire
    ],
    python_requires='>=3.7',

    # Metadata
    description="An enhanced toolkit for deep learning model analysis, profiling, and training optimization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RDTvlokip",
    author_email="rdtvlokip@gmail.com", # Mettre à jour si besoin
    url="https://github.com/RDTvlokip/TrainSense", # Mettre à jour si besoin
    license="MIT", # Garder ceci pour la compatibilité, mais voir la note sur SPDX
    # Optionnel mais recommandé : Spécifier la licence via SPDX identifier
    # license_files = ('LICENSE',), # Si tu as un fichier LICENSE
    keywords=[
        "deep learning", "pytorch", "analysis", "profiling", "optimization",
        "hyperparameters", "gpu", "monitoring", "machine learning", "AI"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License", # Garder pour l'instant, mais l'avertissement persiste
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12", # Ajouter 3.12 vu que tu l'utilises
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Typing :: Typed",
    ],
)