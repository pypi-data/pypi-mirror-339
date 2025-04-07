from setuptools import setup, find_packages

setup(
    name="tum-common-x",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
        "djangorestframework>=3.12.0",  # If you include REST APIs
        # Add other dependencies
    ],
    python_requires=">=3.8",
    description="A reusable tum-common-x application base",
    author="Burak Şen",
    author_email="burak.sen@tum.de",
    # Specify entry points if you have management commands or other CLI tools
    entry_points={
        'console_scripts': [
            'django-base-tool=my_django_base.cli:main',
        ],
    },
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
)