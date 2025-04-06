from setuptools import setup, find_packages

setup(
    name="gtm-healthcheck",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "healthcheck=gtm_healthcheck_automation.gtm_size:main",
        ],
    },
    author="Nipun Patel",
    author_email="nipunp27@gmail.com",
    description="Generic tool to calculate size of each tag, trigger and variable assimilated in a GTM container",
    long_description=open("README.md",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://www.webengage.com/",
    license="MIT",
    license_files=["LICEN[CS]E.*"], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
