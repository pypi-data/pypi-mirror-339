from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.2.7'
DESCRIPTION = 'Titan IMX servo controller'
LONG_DESCRIPTION = Path("./README.md").read_text()


setup(
    name ="ArcusModbus",
    version=VERSION,
    author="Daniel Curtis",
    author_email = "dwc00012@mix.wvu.edu",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    py_modules=['ArcusModbus'],
    install_requires=['pymodbus'],
    keywords=['python','Arcus Titan IMX'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3"
    ]
)