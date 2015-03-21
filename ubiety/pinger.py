import os
import time
import logging
from threading import Thread
from subprocess import call


LOG = logging.getLogger(__name__)


class Pinger(Thread):
    def __init__(self, name, ip, status=False, delay=10, wait=1):
        super(Pinger, self).__init__()
        self.name = name
        self.ip = ip
        self.status = status
        self.delay = delay
        self.wait = wait

    def __repr(self):
        return (
            "Worker('{}', '{}', online={}, delay={})"
            .format(
                self.name,
                self.ip,
                self.online,
                self.delay
            )
        )

    def set_status(self, status):
        """
        Set the online status of the pinger object, depending on the current
        status decide wether to emit a message or not

        :param status: Status to set the pinger instance to
        """
        if status is None:
            raise ValueError("Please specify True or False for status")

        if (not self.status and status):
            LOG.info("{} - {} is online".format(self.name, self.ip))
            self.status = status

        elif (self.status and not status):
            LOG.info("{} - {} went offline".format(self.name, self.ip))
            self.status = status

    def run(self, single_run=False):
        retry = 0
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
                retry += 1
                LOG.debug(
                    "No response from {} - {} increase retry count to {}"
                    .format(self.name, self.ip, retry)
                )

            if result == 1 and retry > 3:
                self.set_status(False)
                retry = 0
            elif result == 0:
                self.set_status(True)
                retry = 0
            time.sleep(self.delay)

    def as_dict(self):
        """
        Returns the current instance as a dict
        """
        result = {
            'name': self.name,
            'ip': self.ip,
            'status': self.status,
            'delay': self.delay,
            'wait': self.wait
        }
        return result

    @staticmethod
    def from_dict(payload):
        result = Pinger(
            payload.get('name', 'NA'),
            payload.get('ip', '127.0.0.1'),
            status=payload.get('status', False),
            delay=payload.get('delay', 10),
            wait=payload.get('wait', 1)
        )
        return result
