from ubiety.pinger import Pinger
from config_resolver import Config
from bottle import Bottle, JSONPlugin
from json import JSONEncoder, dumps as jsonify


class Manager(object):
    def __init__(self, conf=None):
        try:
            self.conf = conf or Config('gefoo', 'ubiety', require_load=True)
            self.pingers = self.create_pingers()

            # Setup restapi
            self.restapi = Bottle()
            self.restapi.get(
                path="/pinger/<pinger_name>",
                callback=self.get_pinger,
                name="get_pinger"
            )
            self.restapi.get(
                path="/pinger",
                callback=self.get_pingers,
                name="get_pingers"
            )
            self.restapi.install(
                JSONPlugin(
                    json_dumps=lambda s: jsonify(s, cls=PingerJSONEncoder)
                )
            )
        except OSError as exc:
            raise OSError(exc)

    def create_pingers(self):
        """
        Create an array of Pinger objects for each `ip_x` definition in the
        config file

        :param conf: Config File to parse for ip definitions
        :returns List of Pinger instances
        """
        delay = self.conf.getint('general', 'delay')
        wait = self.conf.getint('general', 'wait')

        result = dict()
        for section_name in self.conf.sections():
            if "ip_" in section_name:
                name = self.conf.get(
                    section_name,
                    'name',
                    default='No Name defined'
                )
                ip = self.conf.get(
                    section_name,
                    'ip',
                    default='127.0.0.1'
                )
                pinger = Pinger(name.lower(), ip, delay=delay, wait=wait)
                result[pinger.name] = pinger
        return result

    def get_pingers(self):
        result = {
            'pingers': []
        }
        for pinger in self.pingers.values():
            result['pingers'].append(pinger.as_dict())
        return result

    def get_pinger(self, pinger_name):
        """
        Get a specific pinger by it's name

        :param pinger_name: Pinger Name to look up
        """
        result = self.pingers.get(pinger_name.lower())
        if result:
            result = result.as_dict()
        return result


class PingerJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Pinger):
            return obj.as_dict()
        return JSONEncoder.default(self, obj)
