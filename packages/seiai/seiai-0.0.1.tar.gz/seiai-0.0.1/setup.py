
from setuptools import setup, find_packages

setup(
    name="seiai",
    version="0.0.1",
    description="The Future Of AI On Sei",
    author="Teck",
    author_email="Teckdegen@gmail.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.10.5",
        "cosmpy>=0.8.0",
        "langchain>=0.3.0",
        "langchain-openai>=0.2.1",
        "langchain-anthropic>=0.2.1",
        "langchain-google-genai>=0.1.1",
        "langchain-groq>=0.2.1",
        "mnemonic>=0.20"
    ],
    extras_require={
        "dev": ["pytest>=7.4.0"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet"
    ],
    keywords=["blockchain", "sei", "ai", "defi", "chatbot", "p2p", "tokens"],
    license="MIT"
)
