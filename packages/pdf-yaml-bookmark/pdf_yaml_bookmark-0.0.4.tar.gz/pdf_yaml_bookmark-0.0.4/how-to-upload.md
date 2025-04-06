Note: this file should be ignored at global setting (~/.config/git/ignore).

# How to build and upload!
いちいち覚えていないのでメモ。

0. Run tests
1. Increment the version number
2. Build
```
del dist/
python -m build
```

3. Upload
```
python3 -m twine upload dist/*
```
