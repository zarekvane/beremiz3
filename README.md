# Beremiz rewritten with python3.10 and wxpython4

this project is forked from the editor part of 'OpenPLC_Editror', and is rewritten with python3.10.

## needed python library

- wxpython
- lxml
- zeroconf
- pyserial
- gnosis
- compiler
- simplejson
- nevow
- pyjamas

## run this program

```bash
python -B Beremiz.py
```

## Problem

There are a lot of bugs. 

When creating project, the project object has none attribute 'fileHeaders'.

After my trial, I found that it failed to load object and generate some function from xml file, but I don't konw why.

My system os is Arch Linux:

```bash
pacman -S python python-pip
pacman -S wxpython
```
