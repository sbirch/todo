todo
====

Find TODOs in a repo.

This tool works with name-tagged TODOs like these:

```
TODO(sam): fix this

TODO(ben, sam): this is a hack

TODO(sam/jim): make this faster
```

Installation
============

```
pip install todo
```

(This may require permissions to install the `todo` script to your path.)

This tool uses `ack` behind the scenes for fast searching (<a href="http://beyondgrep.com/install/">ack installation</a>.)

Usage
=====

All TODOs in codebase:

`todo`

TODOs by these people:

`todo sam ben`

Count of TODOs by person:

`todo --count`

```
usage: todo [-h] [--count] [NAMES [NAMES ...]]

Find TODOs

positional arguments:
  NAMES       TODO names (any of which is a match). TODO(sam) = sam

optional arguments:
  -h, --help  show this help message and exit
  --count     only print the count
```