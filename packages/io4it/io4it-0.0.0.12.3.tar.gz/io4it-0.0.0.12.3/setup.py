from setuptools import setup, find_packages
import platform
import warnings
# orangecontrib/IO4IT/__init__.py
from setuptools import setup, find_packages
import sys
import subprocess
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation pour l'installation GPU."""
    def run(self):
        install.run(self)  # Installation normale
        
        # Tentative d'installation PyTorch CUDA après l'installation principale
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install',
                'torch', 'torchvision', 'torchaudio',
                '--index-url', 'https://download.pytorch.org/whl/cu126'
            ])
            print("\n\n PyTorch CUDA installé avec succès")
        except subprocess.CalledProcessError:
            print("\n\n IMPORTANT : Pour l'accélération GPU, exécutez MANUELLEMENT:")
            print("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126")


# Nom du package PyPI ('pip install NAME')
NAME = "io4it"

# Version du package PyPI
VERSION = "0.0.0.12.3"  # la version doit être supérieure à la précédente sinon la publication sera refusée

# Facultatif / Adaptable à souhait
AUTHOR = ""
AUTHOR_EMAIL = ""
URL = ""
DESCRIPTION = ""
LICENSE = ""

# 'orange3 add-on' permet de rendre l'addon téléchargeable via l'interface addons d'Orange
KEYWORDS = ["orange3 add-on",]

# Tous les packages python existants dans le projet (avec un __ini__.py)
PACKAGES = find_packages()
PACKAGES = [pack for pack in PACKAGES if "orangecontrib" in pack and "IO4IT" in pack]
PACKAGES.append("orangecontrib")
print("####",PACKAGES)



# Fichiers additionnels aux fichiers .py (comme les icons ou des .ows)
PACKAGE_DATA = {
    "orangecontrib.IO4IT.widgets": ["icons/*", "designer/*"],
}
# /!\ les noms de fichier 'orangecontrib.hkh_bot.widgets' doivent correspondre à l'arborescence

# Dépendances
# Dans votre setup.py principal
INSTALL_REQUIRES = [
    "boto3",
    "docling",
    "docling-core", 
    "speechbrain",
    "whisper",
    "whisper-openai",
    "pyannote.audio",
    "pyannote.core",
    "wave",
    "scikit-learn",
    # NE PAS inclure torch ici
]

# Extras optionnels pour CUDA
EXTRAS_REQUIRE = {
    "cuda": [
        "torch",
        "torchvision",
        "torchaudio"
    ]
}
# Spécifie le dossier contenant les widgets et le nom de section qu'aura l'addon sur Orange
ENTRY_POINTS = {
    "orange.widgets": (
        "Advanced Artificial Intelligence Tools = orangecontrib.IO4IT.widgets",
    )
}
# /!\ les noms de fichier 'orangecontrib.hkh_bot.widgets' doivent correspondre à l'arborescence

NAMESPACE_PACKAGES = ["orangecontrib"]



#   Message informatif si on est sous Windows
if platform.system() == "Windows":
    warnings.warn(
        "Vous êtes sur Windows. Si vous avez une carte NVIDIA CUDA, installez avec :\n"
        "   pip install io4it[cuda] --extra-index-url https://download.pytorch.org/whl/cu126",
        UserWarning
    )


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    keywords=KEYWORDS,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points=ENTRY_POINTS,
    namespace_packages=NAMESPACE_PACKAGES,
    description="Package nécessitant PyTorch CUDA. Après installation, exécutez:\n"
               "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126",
    
    cmdclass={
        'install': PostInstallCommand,
    },
)

