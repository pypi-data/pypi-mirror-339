from setuptools import setup, find_packages

setup(
    name="BwETAF",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flax",
        "jax",
        "huggingface_hub",
        "optax",
        "numpy"
    ],
    description="Module to load BwETAF models (Flax)",
    author="Boring._.wicked",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)