from setuptools import setup, find_packages

setup(
    name="trips_services",  # Your package name
    version="0.2",  # Version number
    packages=find_packages(),  # Automatically find packages
    install_requires=[
        'boto3>=1.26.0',  # List your dependencies here
    ],
    author="mannatsaluja",  # Your name
    author_email="mannatsaluja12@gmail.com",  # Your email
    description="Auto-configured AWS services for Trip Planner",  # A short description
    long_description=open('README.md').read(),  # Read from your README.md for a detailed description
    long_description_content_type="text/markdown",  # If your README is markdown
    url="https://github.com/yourusername/trips_services",  # URL to your project or GitHub
    classifiers=[  # This helps PyPI categorize your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify your supported Python versions
)
