from setuptools import setup, find_packages

setup(
    name="my_image_processor", 
    version="0.1.0",
    description="Um pacote simples para processamento de imagens",
    author="Seu Nome",
    author_email="seu_email@exemplo.com",
    packages=find_packages(),
    install_requires=["pillow"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
