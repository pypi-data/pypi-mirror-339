
from setuptools import setup, find_packages

setup(
    name="borsaiti",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "soundcard",
        "soundfile",
        "mtranslate",
        "ollama",
        "selenium",
        "undetected-chromedriver",
        "speechrecognition"
    ],
    author="Aytunç",
    description="Kick yayınları için AI destekli asistan",
    python_requires=">=3.7",
)
