import setuptools
from pathlib import Path

long_desc = Path("README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="holamundoplayer_javierjaimes",  # ← Nombre único para evitar conflicto
    version="0.0.1",
    long_description=long_desc,
    long_description_content_type="text/markdown",  # opcional pero recomendado
    packages=setuptools.find_packages(
        exclude=["mocks", "tests"]
    ),
)
