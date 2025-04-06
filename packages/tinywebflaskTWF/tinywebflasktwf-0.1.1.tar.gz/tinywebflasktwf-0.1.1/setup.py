from setuptools import setup, find_packages

setup(
    name="tinywebflaskTWF",
    version="0.1.1",
    description="A tiny Python web framework with HTML templating and py-events.",
    author="victor",
    author_email="pradocash8@email.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # Add any needed packages like 'jinja2' if you use it
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.6",
)
