"""Use case: load_config and config"""
""" This file is created by naved001. Use this link to see how he used it https://github.com/CCI-MOC/zabbix-libvirt/tree/master/zabbix_libvirt """

import logging
import logging.handlers
import configparser
config = configparser.ConfigParser()


def get_hosts(hosts_file):
    """Return the IPs/DNS names from a file"""

    with open(hosts_file) as hostfile:
        data = hostfile.read()
    return [item.strip() for item in data.split() if "#" not in item]


def setup_logging(name, logfile):
    """Setup logger with some custom formatting"""
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        logfile, mode="a", maxBytes=5 * 2**20)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def load_config():
    """Load the config file and return the config object"""
    config_file = "./config.ini"
    config.read(config_file)
