from setuptools import setup, find_packages

setup(
    name="aipowershell",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "prompt_toolkit",
        "python-dotenv",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'aipowershell=aipowershell.cli:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered smart shell with command suggestions and natural language processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aipowershell",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
