def get_database(user="jmark", password="nekasifra"):
    from pymongo import MongoClient

    CONNECTION_STRING = f'mongodb+srv://{user}:{password}@two-desperados.uhfws.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)

    return client['two-desperados']

def get_collection(collection_name):
    db = get_database()
    return db[collection_name]