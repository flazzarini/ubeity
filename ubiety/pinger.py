import os
import time
import logging
from threading import Thread
from subprocess import call


LOG = logging.getLogger(__name__)


class Pinger(Thread):
    def __init__(self, name, ip, online=False, delay=10, wait=1):
        super(Pinger, self).__init__()
        self.name = name
        self.ip = ip
        self.online = online
        self.delay = delay
        self.wait = wait
        self.retry = 0

    def __repr__(self):
        return (
            "Pinger('{}', '{}', online={}, delay={}, wait={})"
            .format(
                self.name,
                self.ip,
                self.online,
                self.delay,
                self.wait
            )
        )

    def set_online(self, online):
        """
        Set the ``online`` attribute of the pinger object, depending on the
        current online decide wether to emit a message or not. Once a Pinger
        has become online change the ``delay`` to a higher value.

        :param online: online to set the pinger instance to
        """
        if online is None:
            raise ValueError("Please specify True or False for online")

        if (not self.online and online):
            LOG.info("{} - {} is online".format(self.name, self.ip))
            self.online = online
            self.delay = self.delay * 4

        elif (self.online and not online):
            LOG.info("{} - {} went offline".format(self.name, self.ip))
            self.online = online
            self.delay = self.delay / 4
        return self.online

    def run(self, single_run=False):
        devnull = open(os.devnull, 'w')
        cmd = [
            'ping',
            '-c 1',
            '-W {}'.format(self.wait),
            self.ip,
        ]
        while True:
            LOG.debug("Checking {} - {}".format(self.name, self.ip))
            result = call(cmd, stdout=devnull)

            if result == 1:
                self.retry += 1
                LOG.debug(
                    "No response from {} - {} increase retry count to {}"
                    .format(self.name, self.ip, self.retry)
                )

            if result == 1 and self.retry >= 3:
                self.set_online(False)
                self.retry = 0
            elif result == 0:
                self.set_online(True)
                self.retry = 0

            if single_run:
                break
            time.sleep(self.delay)

    def as_dict(self):
        """
        Returns the current instance as a dict
        """
        result = {
            'name': self.name,
            'ip': self.ip,
            'online': self.online,
            'delay': self.delay,
            'wait': self.wait
        }
        return result

    @staticmethod
    def from_dict(payload):
        result = Pinger(
            payload.get('name', 'NA'),
            payload.get('ip', '127.0.0.1'),
            online=payload.get('online', False),
            delay=payload.get('delay', 10),
            wait=payload.get('wait', 1)
        )
        return result
