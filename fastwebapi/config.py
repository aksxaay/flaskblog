import os

SECRET_KEY = '9fxTuBTb5fNhFCxRiYMkK5QLPfrdz95BXstjpdSG'
API_KEY = 'PKTUJMNISIPH4SUIRND3'
API_URL = 'https://paper-api.alpaca.markets'

DIR = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(DIR)
DB_FILE = os.path.join(BASE_DIR, 'app.db')

resources_dir = os.path.join(BASE_DIR, "images")


TIME_FRAME = ['minute', '5Min','15Min', 'day']



if __name__ == "_main_":
    print(BASE_DIR)
    print(resources_dir)


