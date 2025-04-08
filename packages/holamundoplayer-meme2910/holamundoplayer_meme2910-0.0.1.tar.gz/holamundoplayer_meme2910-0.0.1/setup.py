import setuptools
from pathlib import Path

long_desc = Path("README.md").read_text()

setuptools.setup(
    name="holamundoplayer-meme2910", #Nombre del paquete
    version="0.0.1", #Version
    long_description=long_desc, #Descripcion del paquete
    packages=setuptools.find_packages( #Exclusiones para empaquetado
        exclude=["mocks","tests"]
    )
)