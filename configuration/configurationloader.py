from os.path import join

import yaml

from telegram_parser.settings import BASE_DIR

with open(join(BASE_DIR, 'configuration/config.yaml')) as base:
    configBase = yaml.load(base, Loader=yaml.FullLoader)
    print(configBase)

with open(join(BASE_DIR, 'configuration/config_db.yaml')) as db:
    configDatabase = yaml.load(db, Loader=yaml.FullLoader)
    print(configDatabase)
