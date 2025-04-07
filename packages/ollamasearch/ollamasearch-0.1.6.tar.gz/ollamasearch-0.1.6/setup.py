from setuptools import setup, find_packages

setup(
    name="ollamasearch",
    version="0.1.6", 
    packages=find_packages(),
    install_requires=[
        'requests',
        'platformdirs',
        'sentence-transformers',
        'faiss-cpu',
        'numpy',
        'transformers',
        'accelerate',
    ],
    entry_points={
        "console_scripts": [
            "ollamasearch=ollamasearch.app:main"
        ]
    },
    include_package_data=True,
    description="A Python package for integrating Ollama with web search and RAG.",
    author="Nikhil", 
    author_email="nikhilkhanwani60@gmail.com", 
)
