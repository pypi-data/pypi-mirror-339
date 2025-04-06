from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aipowershell",
    version="0.2.0",  # Updated version
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "prompt_toolkit>=3.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0"
    ],
    entry_points={
        'console_scripts': [
            'aipowershell=aipowershell.cli:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered smart shell with command suggestions and natural language processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aipowershell",
    classifiers=[
        "Development Status :: 4 - Beta",  # Updated from Alpha to Beta
        "Intended Audience :: Developers",
        "Topic :: System :: Shells",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="ai shell cli powershell assistant openai deepseek",  # Updated keywords
    project_urls={
        "Bug Reports": "https://github.com/yourusername/aipowershell/issues",
        "Source": "https://github.com/yourusername/aipowershell",
    },
)


