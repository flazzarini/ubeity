Ubiety
=======

About
-----

A simple presence detection system based on IP addresses. Specify the IP
addresses you want to keep track off, in the configuration file. This program
will then at launch X threads where X is the number of configured IP addresses
to monitor. At fixed intervals defined by ``delay`` value in the configuration
file the program will try to ping the specified IP address. For the sake of this
project we call these running threads ``Pingers``.

An very simple HTTP API has also been included in ``Ubiety`` offering two simple
routes, one to list all available ``Pingers`` and one route to list details of a
specific ``Pinger``.


Configuration File
------------------

The configuration needs to be placed in either one of the following directories

    * ~/.config/gefoo/ubeity/app.ini
    * /etc/gefoo/ubeity/app.ini

Following is a sample configuration file. We defined a ``delay`` of 10 seconds.
Each ping request will have a ping timeout ``wait`` of 4 seconds. We defined two
IP addresses to monitor and give them names. ``port`` defines the TCP Port on
which the HTTP API will be running.


::

    [general]
    delay = 10
    wait = 4
    port = 8080

    [ip_1]
    name = John
    ip = 10.0.0.5

    [ip_2]
    name = Jane
    ip = 10.0.0.6


HTTP API Routes
---------------


[GET] /pinger
~~~~~~~~~~~~~

Returns a list of available ``Pingers`` with their detailed information.

::

    {
        "pingers": [
            {
                "delay": 10,
                "wait": 4,
                "ip": "10.0.0.5",
                "status": true,
                "name": "john"
            },
            {
                "delay": 10,
                "wait": 4,
                "ip": "10.0.0.6",
                "status": true,
                "name": "jane"
           }
        ]
    }


[GET] /pinger/<pinger_name>
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns detailed information of a specific ``Pinger``, specified by it's name.
This query is case insensitive.


::

    {
        "delay": 10,
        "wait": 4,
        "ip": "10.0.0.6",
        "status": true,
        "name": "jane"
    }
