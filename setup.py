from setuptools import setup, find_packages

setup(
    name="gemicli",
    version="1.2.3",
    description="Python package designed for executing simple tasks in the terminal using Gemini AI.",
    author="JamesCoalchi",
    author_email="jamie@jamescoalchi.space",
    packages=find_packages(),
    py_modules=["gemicli"],
    install_requires=[
        "click",
        "google-generativeai"
    ],
    entry_points={
        "console_scripts": [
            "gemicli=gemicli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
