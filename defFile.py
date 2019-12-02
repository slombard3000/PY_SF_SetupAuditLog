import sys

if sys.version_info[0] < 3:
    import ConfigParser as configparser
else:
    import configparser
import requests

Config = configparser.ConfigParser()
Config.read('audit_log_viewer.cnf')
Config.sections()

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1



