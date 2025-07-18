# stockfish-vision/setup.py
from setuptools import setup, find_packages

setup(
    name="stockfish_vision",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "opencv-python",
        "numpy",
        "Pillow"
    ],
)
