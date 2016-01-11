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
```

TODO: Explain commands once they're all implemented.
