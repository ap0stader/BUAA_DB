import json
from redis import Redis

REDIS_CONFIG_FILE = 'redis.json'
rds = None


def init():
    global REDIS_CONFIG_FILE, rds
    with open(REDIS_CONFIG_FILE, 'r') as f:
        config = json.load(f)
    try:
        env = config['environment']
        addr = env['addr']
        port = env['port']
        passwd = env['passwd']
    except Exception as e:
        print("Error reading database config: ", e)
        exit(1)
    try:
        rds = Redis(host=addr, port=port, password=passwd)
    except Exception as e:
        print("Error connecting to database: ", e)
        exit(1)


if __name__ == '__main__':
    init()
    