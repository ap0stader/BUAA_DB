import json
from utils import db, rds

CONF_FILE = 'conf.json'
EXPIRE_TIME_MINUTES = None
JWT_SECRET_KEY = None

def init():
    db.init()
    rds.init()
    with open(CONF_FILE, 'r') as f:
        config = json.load(f)
    
    global EXPIRE_TIME_MINUTES, JWT_SECRET_KEY
    EXPIRE_TIME_MINUTES = config['EXPIRE_TIME_MINUTES']
    JWT_SECRET_KEY = config['JWT_SECRET_KEY']
