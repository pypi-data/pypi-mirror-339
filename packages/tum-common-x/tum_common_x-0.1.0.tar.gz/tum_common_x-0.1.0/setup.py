from setuptools import setup, find_packages

setup(
    name="tum-common-x",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
        # Add other dependencies
    ],
    description="A reusable tum-common-x application",
    author="Burak Şen",
    author_email="burak.sen@tum.de",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",  # Update as needed
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",  # Choose your license
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",  # Update as needed
    ],
)