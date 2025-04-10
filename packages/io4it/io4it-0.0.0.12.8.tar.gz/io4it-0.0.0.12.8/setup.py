import time
import warnings
from setuptools import setup, find_packages
import sys
import subprocess
import platform
from setuptools.command.install import install

def log_message(message, level="INFO"):
    timestamp = time.strftime("%H:%M:%S")
    border = "=" * (len(message) + 4)
    print(f"\n{border}")
    print(f"{timestamp} - {level} - {message}")
    print(f"{border}\n")

class CustomInstall(install):
    def run(self):
        log_message(f"Début de l'installation de {NAME} v{VERSION}")
        
        # Installation des dépendances de base
        log_message("Étape 1/2 : Installation des dépendances principales")
        install.run(self)
        
        # Gestion CUDA si option spécifiée
        if 'cuda' in sys.argv:
            log_message("Option [cuda] détectée", "IMPORTANT")
            self._install_torch_cuda()
        else:
            log_message("Mode CPU sélectionné", "NOTE")
            self._warn_cuda_option()

    def _install_torch_cuda(self):
        try:
            log_message("Vérification de l'environnement CUDA...")
            import torch
            if torch.cuda.is_available():
                log_message(f"PyTorch CUDA déjà installé (v{torch.__version__}, CUDA v{torch.version.cuda})", "SUCCÈS")
                return
            else:
                log_message("PyTorch installé mais CUDA non disponible", "AVERTISSEMENT")
        except ImportError:
            log_message("PyTorch non détecté", "INFO")

        log_message("Tentative d'installation de PyTorch avec CUDA 12.6...", "IMPORTANT")
        try:
            cmd = [
                sys.executable, '-m', 'pip', 'install',
                'torch==2.6+cu126',
                'torchvision==0.17.2+cu126',
                'torchaudio==2.6+cu126',
                '--index-url', 'https://download.pytorch.org/whl/cu126',
                '--no-deps'
            ]
            log_message(f"Commande exécutée: {' '.join(cmd)}", "DEBUG")
            
            start_time = time.time()
            subprocess.check_call(cmd)
            duration = time.time() - start_time
            
            log_message(f"PyTorch CUDA installé avec succès en {duration:.1f}s", "SUCCÈS")
            
            # Vérification finale
            import torch
            log_message(f"Version PyTorch: {torch.__version__}", "INFO")
            log_message(f"Version CUDA: {torch.version.cuda}", "INFO")
            log_message(f"Disponibilité CUDA: {torch.cuda.is_available()}", "INFO")
            
        except subprocess.CalledProcessError as e:
            log_message("ÉCHEC de l'installation CUDA", "ERREUR")
            log_message("Solution alternative:", "IMPORTANT")
            print("\n\033[93m" + "="*80)
            print("POUR INSTALLER MANUELLEMENT PYTORCH CUDA, EXÉCUTEZ:")
            print("pip install torch==2.2.2+cu126 torchvision==0.17.2+cu126 torchaudio==2.2.2+cu126")
            print("--index-url https://download.pytorch.org/whl/cu126")
            print("="*80 + "\033[0m\n")

    def _warn_cuda_option(self):
        if platform.system() == "Windows":
            log_message("ASTUCE: Pour activer CUDA sous Windows", "NOTE")
            print("\033[94m" + "="*80)
            print("Pour une version avec accélération GPU, utilisez plutôt:")
            print("pip install io4it[cuda] --extra-index-url https://download.pytorch.org/whl/cu126")
            print("="*80 + "\033[0m\n")


# Configuration
NAME = "io4it"
VERSION = "0.0.0.12.8"  # Incrémentez la version

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

EXTRAS_REQUIRE = {
    'cuda': [
        'torch==2.6+cu126; sys_platform == "win32"',
        'torchvision==0.17.2+cu126; sys_platform == "win32"',
        'torchaudio==2.6+cu126; sys_platform == "win32"'
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
    entry_points=ENTRY_POINTS,
    namespace_packages=NAMESPACE_PACKAGES,
    cmdclass={
        'install': CustomInstall,
    },
)

