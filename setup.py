import sys
from cx_Freeze import setup, Executable

setup(name="Demo",
    version="0.1",
    description="Image type selector",
    author="Sangwon Lee",
    executables=[Executable("ImageTypeSelector.py", base="Win32GUI")])

## >python setup.py build