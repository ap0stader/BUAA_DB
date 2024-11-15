import json, pymysql

DB_CONFIG_FILE = 'db.json'
config = None

db_pool = {}

def init():
    global DB_CONFIG_FILE, config
    with open(DB_CONFIG_FILE, 'r') as f:
        config = json.load(f)
    for user in config['users']:
        db_pool[user] = connect(user)

def connect(user):
    global config
    try:
        env = config['users'][user]
        addr = env['addr']
        port = env['port']
        passwd = env['passwd']
    except Exception as e:
        print("Error reading database config: ", e)
        return None
    try:
        return pymysql.connect(
            host=addr,
            port=port,
            user=user,
            password=passwd,
            database='data'
        )
    except Exception as e:
        print("Error connecting to database: ", e)
        return None

def get_cursor(user):
    global db_pool
    if user in db_pool:
        return db_pool[user].cursor(pymysql.cursors.DictCursor)
    else:
        return None

if __name__ == '__main__':
    init()
