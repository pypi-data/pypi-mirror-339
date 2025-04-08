from setuptools import setup, find_packages
import platform


# Nom du package PyPI ('pip install NAME')
NAME = "io4it"

# Version du package PyPI
VERSION = "0.0.0.10"  # la version doit être supérieure à la précédente sinon la publication sera refusée

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
INSTALL_REQUIRES = ["boto3", "docling", "docling-core", "speechbrain", "whisper", "whisper-openai", "pyannote.audio", "pyannote.core", "wave", "scikit-learn"]



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
    print("  Vous êtes sur Windows. Si vous avez une carte NVIDIA CUDA, vous pouvez installer les dépendances optimisées avec :")
    print("   pip install io4it[cuda] --extra-index-url https://download.pytorch.org/whl/cu126")



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
    extras_require=EXTRAS_REQUIRE,
    entry_points=ENTRY_POINTS,
    namespace_packages=NAMESPACE_PACKAGES,
)

