from setuptools import setup, find_packages
import sys
import logging

from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        try:
            import torch
            if not torch.cuda.is_available():
                import subprocess
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install',
                    '--extra-index-url', 'https://download.pytorch.org/whl/cu126',
                    'torch', 'torchvision', 'torchaudio'
                ])
        except ImportError:
            pass

# Configure le logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


# Nom du package PyPI ('pip install NAME')
NAME = "IO4IT"

# Version du package PyPI
VERSION = "0.0.0.11.2"  # la version doit être supérieure à la précédente sinon la publication sera refusée

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
    "scikit-learn"
]

# Spécifie le dossier contenant les widgets et le nom de section qu'aura l'addon sur Orange
ENTRY_POINTS = {
    "orange.widgets": (
        "Advanced Artificial Intelligence Tools = orangecontrib.IO4IT.widgets",
    )
}
# /!\ les noms de fichier 'orangecontrib.hkh_bot.widgets' doivent correspondre à l'arborescence

NAMESPACE_PACKAGES = ["orangecontrib"]

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    license=LICENSE,
    keywords=KEYWORDS,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    install_requires=INSTALL_REQUIRES,
    entry_points=ENTRY_POINTS,
    namespace_packages=NAMESPACE_PACKAGES,
    cmdclass={
        'install': PostInstallCommand,
    },
    python_requires='>=3.8',  # Spécifiez votre version minimale de Python
)
