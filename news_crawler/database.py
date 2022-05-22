from pymongo import ASCENDING
import config

def get_database():
    from pymongo import MongoClient

    user, password = config.connection
    CONNECTION_STRING = f'mongodb+srv://{user}:{password}@two-desperados.uhfws.mongodb.net/?retryWrites=true&w=majority'
    
    client = MongoClient(CONNECTION_STRING)
    return client['two-desperados']

def insert_articles(data):
    db = get_database()
    articles_col = db['articles']

    articles_col.insert_many(data)
    articles_col.create_index([("keywords", ASCENDING)])
