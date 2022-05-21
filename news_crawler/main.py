import sys, json
import config
import database as db

def load_articles():
    with open(config.article_path, 'r') as f:
        articles_data = json.load(f)
    return articles_data

def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print("Invalid number of arguments!")
        return

    config.connection['user'] = args[0]
    config.connection['password'] = args[1]
    articles_data = load_articles()
    db.insert_articles(articles_data)

main()
