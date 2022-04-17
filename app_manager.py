from datetime import datetime
from pymongo import MongoClient
from config import URL_MONGO

try:
    client = MongoClient(URL_MONGO)
    database = client['urlshortener']
    collection = database['urls']
except:
    print('Error to connect in Mongo')

def register_url(url, token):

    global collection

    try:

        document = {
            'url' : url,
            'token': token,
            'viewers': 0,
            'timestamp-visits': []
        }

        collection.insert_one(document)

    except:
        print('Error insert URL in database')

def check_token(token):
    global collection

    try:

        document = {
            'token': token
            }

        search = list(collection.find(document))

        if len(search) > 0:
            return True

        else:
            return False

    except:
        print('Error check token in database')

def go_to_the_page(token):

    global collection

    try:

        timestamp = get_timestamp()

        filter = {
            'token': token
            }

        update = {
            '$inc' : { "viewers" : 1 },
            '$push': {'timestamp-visits': timestamp}
            }

        search = collection.find_one_and_update(filter, update)

        url = search['url']

        if ('http://' in url) or ('https://' in url):
            pass
        else:
            url = f'http://{url}'

        return f'<head><meta http-equiv="refresh" content="5; url={url}"></head>'

    except:
        print('Error check token in database')

def get_all_urls():

    global collection

    try:

        raw_reponse = list(collection.find({}))
        data = []

        for item in raw_reponse:
            del item['_id']

            data.append(item)
        

        return data

    except:
        print('Error check items in database')

        

def delete_url_database(token):

    global collection

    try:

        token_page = {
            'token': token
            }

        search = collection.delete_one(token_page)

        return f'This url with token {token} is delete from database'

    except:
        print('Error delete document in database')

def get_timestamp():

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    return timestamp
