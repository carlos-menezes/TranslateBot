import configparser
import os

configParser = configparser.RawConfigParser()
configFilePath = os.path.join(os.path.dirname(__file__), 'config.cfg')
configParser.read(configFilePath)

yandex_api = configParser.get("yandex", "api")

