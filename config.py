from configparser import ConfigParser

ConfFile = '/etc/odoo-prd/sender.conf'

def odoo_config(_filename, _section):
    parser = ConfigParser()
    parser.read(_filename)
