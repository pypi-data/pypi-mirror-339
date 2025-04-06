from setuptools import setup, find_packages

setup(
    name="graph_games_model_runner",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "multipledispatch==1.0.0",
        "torch==2.2.0",
        "torch-geometric==2.3.1",
        "graph-games-proto==0.3.595",
    ],
)