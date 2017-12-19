# README.md
1. How to install needed library

```
pip install PyQt5
pip install PyQt5-tools
pip install pyinstaller
pip install pandas
```

2. How to convert pyqt designer .ui file to .py file.
```
pyuic5 selector.ui -o selectorUI.py
```

3. How to make exe file.
```
pyinstaller -F ImageTypeSelector.spec
```
