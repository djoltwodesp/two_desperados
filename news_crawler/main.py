import json

def get_database():
    from pymongo import MongoClient

    CONNECTION_STRING = 'mongodb+srv://jmark:nekasifra@two-desperados.uhfws.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)

    return client['two-desperados']


def get_articles():
    with open('news/test.json', 'r') as f:
        articles_data = json.load(f)
    return articles_data

def insert_articles(data):
    #index by name
    db = get_database()
    articles_col = db['articles']

    articles_col.insert_many(data)

def main():
    articles_data = get_articles()
    insert_articles(articles_data)

main()