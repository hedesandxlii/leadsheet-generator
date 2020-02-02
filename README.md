## Text to leadsheet

This project is used to convert a basic file to a lead sheet in pdf. For example should

```
Am F C G
```

Be converted into a nicely printed PDF, which can be used in a live setting.


### Running the script
ATM, the script is produces a static PDF with the chords to Galenskaparna's *Macken*. This is
subject to change.

**Running the program:**
```
$ python leadsheet.py
```

**Running tests:**
```
$ pytest 
```

**Running tests with `Coverage.py`:**
```
// Get coverage reported in a html format in `htmlcov` folder
$ coverage html --include=./*

// Get coverage reported in the terminal
$ coverage report --include=./*
```
