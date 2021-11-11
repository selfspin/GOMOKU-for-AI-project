# GOMOKU for AI project

DATA130008, School of Data Science, Fudan University

## pbrain-pyrandom

#### A Python Piskvork template

**pbrain-pyrandom** is the technical core of a "brain" (AI) for [Piskvork gomoku manager](http://petr.lastovicka.sweb.cz/piskvork.zip)
used in [Gomocup AI tournament](http://gomocup.org), written in Python.

The code is basically the "Python copy" of [C++ template](http://petr.lastovicka.sweb.cz/skel_cpp.zip) written by [Petr Lastovicka](http://petr.lastovicka.sweb.cz/indexEN.html).
This README is also partially copy of the C++ template's README.

#### Prerequisites and compilation
The Piskvork manager is a Win32 application and currently supports only Win32 compatible .exe files (furthermore whose name starts with pbrain- prefix).
There are several ways how to create .exe from Python files.

Here I present the approach using [PyInstaller](http://pyinstaller.org) and Windows command line:

1. Install Windows (or [Wine](https://www.winehq.org/) for Linux, originally the project was created and tested on Ubuntu 16.04 using Wine)
2. Install [Python](http://www.python.org) (the code and also following instructions were tested with versions 2.7 and 3.6).
3. Install [pywin32](https://sourceforge.net/projects/pywin32) Python package: `pip.exe install pypiwin32` (if not present "by default")
4. Install [PyInstaller](https://www.pyinstaller.org/): `pip.exe install pyinstaller`

To compile the example, use the following command line command:
```
cd C:\path\where\the\files\were\saved
pyinstaller absearch.py pisqpipe.py --name pbrain-absearch.exe --onefile
```

Note: the executables `pip.exe` and `pyinstaller.exe` might need full path, in my case I used `C:\Python27\Scripts\pip.exe` and `C:\Python27\Scripts\pyinstaller.exe`.

#### How to create your own AI
Replace file example.py with your own algorithm. Please don't change file pisqpipe.py, because it contains communication between your AI and the game manager and it might be changed in future protocol versions. 
More information about the protocol and tournament rules can be found at [Gomocup websites](http://gomocup.org)

## alpha beta pruning

absearch
胜局：25=11+14，负局：11=7+4
每手棋用时：986毫秒（最多12.9秒），每局用时：18秒
每局手数：18，CRC值：3a3b4726，内存：4.15MB

![image-20211111234729312](C:\Users\姜\AppData\Roaming\Typora\typora-user-images\image-20211111234729312.png)

