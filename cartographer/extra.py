from klippy import configfile

from cartographer.scanner import PrinterScanner


def load_config(config: configfile.ConfigWrapper):
    return PrinterScanner(config)
