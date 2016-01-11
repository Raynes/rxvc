# rxvc

A superfast command line controller for Yamaha RX-V series
receivers. It's written targeting Python 3.5>, and uses the
excellent [rxv](https://github.com/wuub/rxv) library to
function.

The key reason I wanted this is because the RX-V477's web
interface appears to not feature a way to control inputs
and volume like my old RX-V675 did.

However, because the thing lives at a random place on your
network, finding the receiver can cause CLI tools like this
to be quite slow due to the fact that `rxv` has to use SSDP
to find the IP of the receiver. `rxvc` gets around this by
caching the receiver control url and name info to
`~/.rxvc_cache` on the first run of a command. This cache
can be cleared with a command line flag.

## Usage

This is a Python 3 project. I'm using this on 3.5, and am
not trying to support older versions of Python. Check out
[pyenv](https://github.com/yyuu/pyenv) if you need an easy
way to get 3.5, or if on a mac you can just use homebrew.

With Python 3 (probably in a pyvenv virtual environment),
you can install `rxvc` with pip:

```
$ pip install rxvc
$ rxvc --help
Usage: rxvc [OPTIONS] COMMAND [ARGS]...

  Control your Yamaha receiver from the command line, really fast.

  Taking advantage of caching (which can be cleared buy running rxvc with no
  command but with --clear), after the first run it's super fast. This cache
  is stored in ~/.rxvc_cache.

  Have fun!

Options:
  --clear     Clear the cache and look for receivers again.
  -h, --help  Show this message and exit.

Commands:
  down    Turn down the receiver volume in 0.5...
  input   See the current receiver input or set it if...
  inputs  List valid input names for this receiver.
  power   Power the receiver on or off.
  status  Print overall status of the receiver.
  up      Turn up the receiver volume in 0.5...
  volume  Show the current receiver volume level, or...
```

## Volume

The way volume works might confuse you at first. There are three
commands for controlling volume, `volume`, `up`, and `down`.

The lowest level command is the `volume` command. It can be used
to simply print current volume or set it to an absolute number
with the `-v` option. Keep in mind that these receivers only accept
volume levels as negative numbers in `-0.5` increments, so an error
will be printed if you tried to do something like this:

```
$ rxvc volume -v -40.2
Volume must be specified in -0.5 increments.
$ rxvc volume -v 39.5
Volume must be specified in -0.5 increments.
$ rxvc volume -v -39.5
-39.5
```

The last command is correct and the others are error cases.

In addition to this low level `volume` command there are easier
to use commands, `up`, and `down`, for adjusting volume
incrementally. They work on a concept of 'points'. You simply
pass an integer to them and it gets multiplied by `0.5` and added
or subtracted from the current volume level and the new level is
printed unless the receiver responds with an error (presumably
due to the new volume level being out of range).

`up` and `down` default to 2 points, which would result in an
increase or decrease of `1.0` respectively. Here are some examples:

```
$ rxvc up
-38.5
$ rxvc down
-39.5
$ rxvc up 3
-38.0
$ rxvc down 3
-39.5
$ rxvc down 1000000
New volume must be out of range.
```
