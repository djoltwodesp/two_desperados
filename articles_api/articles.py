from flask import Flask
from flask import url_for
import database as db
from bson.objectid import ObjectId

def parse_article(article):
    url = article["article_url"]
    title = article["title"]
    author = article["author"]
    heading = f'<h1><a href="{url}">{title}</a></h1><h4>By {author}</h4>'

    content = ""
    for c in article["content"]:
        if isinstance(c, str):
            content += f'<p>{c}</p>'
        elif isinstance(c, dict):
            src = f"{c['src']}"
            content += f'<img src={src}>'
    return heading + content

def parse_articles(articles):
    res = ""
    for a in articles:
        o_id = a["_id"]
        url = url_for('get_by_id', id=o_id)
        title = a["title"]
        author = a["author"]
        heading = f'<h2><a href="{url}">{title}</a></h2><h4>By {author}</h4>'
        res += heading + "<hr>"
    return res

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
    <p>Possible routes:</p>
    <ul>
        <li>All articles: <b>/all</b></li>
        <li>Articles by keyword: <b>/key/:keyword:</b></li>
        <li>Article by id: <b>/id/:id:</b></li>
    </ul>
    """

@app.route("/all")
def get_all():
    articles_collection = db.get_collection("articles")
    articles = articles_collection.find()
    return parse_articles(articles)

@app.route("/key/<keyword>")
def get_by_keyword(keyword):
    articles_collection = db.get_collection("articles")
    articles = articles_collection.find({'keywords': keyword})
    return parse_articles(articles)

@app.route("/id/<id>")
def get_by_id(id):
    articles_collection = db.get_collection("articles")
    try:
        article = articles_collection.find_one({'_id': ObjectId(id)})
        return parse_article(article)
    except:
        return "<h3>invalid argument or object doesn't exist</h3>"
