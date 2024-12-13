from klippy import configfile

from .scanner import PrinterScanner


def load_config(config: configfile.ConfigWrapper):
    return PrinterScanner(config)
