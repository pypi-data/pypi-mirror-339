from setuptools import setup, find_packages

setup(
    name="eziql",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "groq",
        "python-dotenv"
    ],
    author="Aman Prajapat",
    author_email="prajapataman007@gmail.com",
    description="Generate SQL queries from natural language using Groq's LLaMA model.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aman-prajapat/eziql", 
    license="MIT", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
