# Fast Transfer

An easy and fast way to transfer files between mulitple users.
If you frequently run the command `python -m http.server`, you will like it.


## Usage

Share a full path directory
```
fast-transfer /tmp
```

Share a relative path directory
```
fast-transfer demo
```

Then, you can visit the website at `http://192.168.x.x:5000`


## Installation

```
pip install fast-transfer
```

## OPTIONS

```
Usage: fast-transfer [OPTIONS] USERDATA

Options:
  -p, --port INTEGER  The port to bind to.  [default: 5000]
  --help              Show this message and exit.
```
