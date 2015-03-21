from ubiety.manager import Manager
import logging
import time
from threading import Thread


LOG = logging.getLogger(__name__)


def main():
    try:
        man = Manager()
        host = man.conf.get('general', 'host', default='localhost')
        port = man.conf.getint('general', 'port')

        LOG.info("Starting RestAPI on Port {}".format(port))
        restapithread = Thread(
            target=man.restapi.run,
            kwargs={
                'host': host,
                'port': port
            }
        )
        restapithread.daemon = True
        restapithread.start()

        LOG.info("Starting all pingers")
        for pinger in man.pingers.values():
            LOG.info("Start Pinger for {}".format(pinger.name))
            pinger.daemon = True
            pinger.start()

        while pinger.isAlive():
            time.sleep(0.2)

        for pinger in man.pingers.values():
            pinger.join(1)

    except OSError as exc:
        LOG.error("No config file found - {}".format(exc))
    except KeyboardInterrupt as exc:
        LOG.info("Stopping...")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
