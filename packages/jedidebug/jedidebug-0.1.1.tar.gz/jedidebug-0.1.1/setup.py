from setuptools import setup, find_packages

setup(
    name="jedidebug",
    version="0.1.1",
    packages=find_packages(),
    description="A library that motivates programmers with Star Wars quotes when their code has bugs",
    long_description="""
        JediDebug is a lighthearted Python library that catches exceptions and provides
        motivational Star Wars-themed wisdom. Perfect for keeping spirits high during
        frustrating debugging sessions and adding a touch of the Force to your development workflow.
    """,
    author="NotaRealProgrammer",
    author_email="notarealprogrammer010@gmail.com",
    url="https://github.com/notarealprogrammer001/jedidebug",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)