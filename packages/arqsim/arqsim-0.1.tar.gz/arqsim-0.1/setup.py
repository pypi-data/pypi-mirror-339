from setuptools import setup, find_packages

setup(
    name="arqsim",
    version="0.1",
    description="Simulate ARQ protocols: Stop-and-Wait, Go-Back-N, Selective Repeat",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "arqsim=arqsim.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)
