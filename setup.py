from setuptools import setup, find_packages

setup(
    name="tcs-app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3",
        "pandas==2.2.0",
        "numpy==1.26.4",
        "openpyxl==3.1.2",
        "python-dotenv==1.0.0",
        "Werkzeug==2.3.7",
        "Pillow==10.2.0",
        "gunicorn==21.2.0",
    ],
    python_requires=">=3.11",
) 