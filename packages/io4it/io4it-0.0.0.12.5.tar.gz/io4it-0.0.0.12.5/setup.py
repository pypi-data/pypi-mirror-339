from setuptools import setup, find_packages
import platform
import warnings
# orangecontrib/IO4IT/__init__.py
from setuptools import setup, find_packages
import sys
import subprocess
from setuptools.command.install import install

from setuptools import setup, find_packages
import sys
import subprocess
import platform
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        # Installation normale d'abord
        install.run(self)
        
        # Vérification CUDA seulement sur Windows
        if platform.system() == "Windows":
            self._install_torch_cuda()

    def _install_torch_cuda(self):
        try:
            import torch
            if torch.cuda.is_available():
                print("\n PyTorch CUDA est déjà installé et fonctionnel")
                return
        except ImportError:
            pass

        print("\n\n Tentative d'installation de PyTorch CUDA 12.6...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install',
                'torch==2.2.2+cu126',
                'torchvision==0.17.2+cu126', 
                'torchaudio==2.2.2+cu126',
                '--index-url', 'https://download.pytorch.org/whl/cu126',
                '--no-deps'  # Évite de réinstaller les dépendances existantes
            ])
            print("\n\n PyTorch CUDA installé avec succès")
        except subprocess.CalledProcessError:
            print("\n\n ÉCHEC de l'installation automatique de PyTorch CUDA")
            print("Veuillez exécuter MANUELLEMENT cette commande :")
            print("pip install torch==2.2.2+cu126 torchvision==0.17.2+cu126 torchaudio==2.2.2+cu126 --index-url https://download.pytorch.org/whl/cu126")

# Configuration
NAME = "io4it"
VERSION = "0.0.0.12.5"  # Incrémentez la version

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
    # Exclure torch intentionnellement
]
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
    entry_points=ENTRY_POINTS,
    namespace_packages=NAMESPACE_PACKAGES,
    cmdclass={
        'install': CustomInstall,
    },
)

