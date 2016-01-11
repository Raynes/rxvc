"""Functions for working with our receiver cache."""
import json
from pathlib import Path
from os.path import expanduser
from rxv import RXV

cache_path = Path(expanduser("~/.rxvc_cache"))


def cache_receiver(receiver):
    """Touch our cache file to make sure it at least exists and
    dump what we know (control url, name, model) to json into
    the file as a cache for the next run of this project.

    """
    cache_path.touch(exist_ok=True)
    cache_path.write_text(json.dumps({
        'ctrl_url': receiver.ctrl_url,
        'friendly_name': receiver.friendly_name,
        'model_name': receiver.model_name}))


def cached_receiver():
    """Return an RXV object for our cached receiver if there
    is one otherwise return None and the cache will be populated
    on the next run of rxvc.

    """
    if cache_path.exists():
        parsed_cache = json.loads(cache_path.read_text())
        return RXV(parsed_cache['ctrl_url'],
                   friendly_name=parsed_cache['friendly_name'],
                   model_name=parsed_cache['model_name'])


def clear():
    """Clear the receiver cache if it exists."""
    if cache_path.exists():
        cache_path.unlink()
