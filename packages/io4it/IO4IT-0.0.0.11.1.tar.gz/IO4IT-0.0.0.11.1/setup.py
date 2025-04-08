from setuptools import setup, find_packages
import sys
import logging

from setuptools.command.install import install

class CustomInstallCommand(install):
    """Classe d'installation personnalisée avec gestion de PyTorch."""
    
    def _install_torch_with_cuda(self):
        """Tente d'installer PyTorch avec support CUDA."""
        try:
            import torch
            if torch.cuda.is_available():
                logger.info("✅ PyTorch avec CUDA est déjà installé")
                return True
                
            logger.info("🔄 Tentative d'installation de PyTorch avec CUDA 12.6...")
            
            # Installation directe via les wheels PyTorch
            import subprocess
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install',
                '--extra-index-url', 'https://download.pytorch.org/whl/cu126',
                'torch', 'torchvision', 'torchaudio'
            ])
            
            # Vérification après installation
            import torch
            if torch.cuda.is_available():
                logger.info("🎉 PyTorch avec CUDA installé avec succès!")
                return True
            else:
                logger.warning("⚠️ PyTorch installé mais CUDA non disponible")
                return False
                
        except Exception as e:
            logger.error(f"❌ Échec de l'installation avec CUDA: {str(e)}")
            return False
    
    def _install_torch_cpu(self):
        """Fallback: installe la version CPU de PyTorch."""
        try:
            logger.info("🔄 Installation de la version CPU de PyTorch...")
            import subprocess
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install',
                'torch', 'torchvision', 'torchaudio',
                '--index-url', 'https://download.pytorch.org/whl/cpu'
            ])
            logger.info("🔶 PyTorch (CPU) installé avec succès")
            return True
        except Exception as e:
            logger.error(f"❌ Échec de l'installation CPU: {str(e)}")
            return False
    
    def run(self):
        # Tentative d'installation avec CUDA d'abord
        if not self._install_torch_with_cuda():
            logger.warning("Tentative de fallback avec version CPU...")
            self._install_torch_cpu()
        
        # Installation normale des autres dépendances
        install.run(self)

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
VERSION = "0.0.0.11.1"  # la version doit être supérieure à la précédente sinon la publication sera refusée

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
    "scikit-learn",
    "torch @ https://download.pytorch.org/whl/cu126/torch-2.1.2%2Bcu126-cp311-cp311-win_amd64.whl",
    "torchvision @ https://download.pytorch.org/whl/cu126/torchvision-0.16.2%2Bcu126-cp311-cp311-win_amd64.whl",
    "torchaudio @ https://download.pytorch.org/whl/cu126/torchaudio-2.1.2%2Bcu126-cp311-cp311-win_amd64.whl"
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
        'install': CustomInstallCommand,
    },
    python_requires='>=3.8',  # Spécifiez votre version minimale de Python
)
