from setuptools import setup, find_packages


setup(
    name="automation-db",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "automation_prompt=automation_db.main:main" 
        ],
    },
    python_requires=">=3.7",
)
