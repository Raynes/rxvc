import json
from pathlib import Path
from os.path import expanduser
from rxv import RXV

cache_path = Path(expanduser("~/.rxvc_cache"))


def cache_receiver(receiver):
    cache_path.touch(exist_ok=True)
    cache_path.write_text(json.dumps({
        'ctrl_url': receiver.ctrl_url,
        'friendly_name': receiver.friendly_name,
        'model_name': receiver.model_name}))


def cached_receiver():
    if cache_path.exists():
        parsed_cache = json.loads(cache_path.read_text())
        return RXV(parsed_cache['ctrl_url'],
                   friendly_name=parsed_cache['friendly_name'],
                   model_name=parsed_cache['model_name'])


def clear():
    if cache_path.exists():
        cache_path.unlink()
