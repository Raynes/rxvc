"""Safe abstraction over RXV handling reconnection when necessary."""
import sys
import json
from pathlib import Path
from os.path import expanduser
import requests.exceptions
from rxv import RXV
import rxv
from rxvc.config import Config
from retry import retry


class ReceiverNotFoundException(Exception):
    pass


config = Config()
log = config.logger(__name__)


class RXVC(object):
    """Wrapper around the rxv library to provide reconnection support
    for RXV objects.

    """
    def __init__(self, retrying=True):
        self.cache_path = Path(expanduser("~/.rxvc_cache"))
        self.retrying = retrying

        # Make sure we get a receiver cached at init.
        self.rxv

    def _test_rxv(self, receiver):
        """Test our connection to a receiver."""
        try:
            log.debug("Testing receiver connection")
            status = receiver.basic_status
            log.debug(("Connection test successful, "
                            "status is: {}").format(status))
            return True
        except requests.exceptions.ConnectionError:
            log.error("Connection test unsuccessful.")
            return False

    @property
    def rxv(self):
        """Return a receiver.

        If the receiver is cached, it is tested with a basic status
        call and if successful it is returned. If the test is not
        successful, we try to look for receivers again, and if one
        is found we cache it.


        """
        receiver = self.cached_receiver
        if receiver:
            if self._test_rxv(receiver):
                return receiver
            else:
                self.clear()
                receiver = self.find_receiver()
                self.cache_receiver(receiver)
                return receiver
        else:
            receiver = self.find_receiver()
            self.cache_receiver(receiver)
            return receiver

    @retry(delay=5, exceptions=ReceiverNotFoundException, logger=log)
    def find_receiver(self):
        """Look for a receiver using rxv's find method. If no receiver
        is found, retry until one is found. If retry=False is set,
        we simply give up and exit.

        """
        receiver = None
        log.info("Looking for receivers...")
        found_receivers = rxv.find()
        if len(found_receivers) == 1:
            log.info("Found multiple receivers, choosing the first one.")
            receiver = found_receivers[0]
            log.info("Using {}".format(receiver.friendly_name))
            self.cache_receiver(receiver)
        elif (not found_receivers) and self.retrying:
            raise ReceiverNotFoundException("No receiver found.")
        elif not found_receivers:
            log.error("No receiver found, giving up")
            sys.exit(1)
        else:
            receiver = found_receivers[0]
            log.info(
                "Found receiver: {}".format(receiver.friendly_name)
            )

        return receiver

    def cache_receiver(self, receiver):
        """Touch our cache file to make sure it at least exists and
        dump what we know (control url, name, model) to json into
        the file as a cache for the next run of this project.

        """
        self.cache_path.touch(exist_ok=True)
        self.cache_path.write_text(json.dumps({
            'ctrl_url': receiver.ctrl_url,
            'friendly_name': receiver.friendly_name,
            'model_name': receiver.model_name}))

    @property
    def cached_receiver(self):
        """Return an RXV object for our cached receiver if there
        is one otherwise return None and the cache will be populated
        on the next run of rxvc.

        """
        if self.cache_path.exists():
            parsed_cache = json.loads(self.cache_path.read_text())
            return RXV(parsed_cache['ctrl_url'],
                       friendly_name=parsed_cache['friendly_name'],
                       model_name=parsed_cache['model_name'])

    def clear(self):
        """Clear the receiver cache if it exists."""
        if self.cache_path.exists():
            self.cache_path.unlink()
