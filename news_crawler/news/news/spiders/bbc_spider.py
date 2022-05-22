import scrapy
from scrapy.crawler import CrawlerProcess
from summa import keywords
import re

bbc_home_url = "https://www.bbc.com"
home_url = "https://www.bbc.com"

def parse_homepage(response):
    links = response.css('a')

    pattern = re.compile(r'^\/.*(\d{2,})$')
    conditions = lambda a: a and pattern.match(a) and not '/live/' in a and '/news/' in a

    article_urls = {bbc_home_url + a for a in [a.attrib['href'] for a in links] if conditions(a)}
    return article_urls

def parse_article(response):
    article = response.xpath('descendant-or-self::article')

    url = response.url
    author = article.css('strong::text').get()
    if not author:
        author = "unknown"
    title = article.css('h1::text').get()
    article_content = parse_article_content(article)
    return url, author, title, article_content

def parse_article_content(article):
    article_content = []

    blocks = article.xpath('./div[@data-component="text-block"]|./div[@data-component="image-block"]')
    for a_block in blocks:
        data_component = a_block.css('div::attr(data-component)').extract_first()
        block = None
        
        if data_component == "image-block":
            block = {}
            block["src"] = a_block.css('img::attr(src)').extract_first()
            block["caption"] = a_block.css('div[class="ssrcss-y7krbn-Stack e1y4nx260"]::text').extract_first()
        elif data_component == "text-block":
            block = a_block.xpath('string(.)').extract_first()
        
        if block:
            article_content.append(block)
    
    return article_content

def suma_extractor(title, content):
    text = title + " "
    for c in content:
        if isinstance(c, str):
            text += c + " "
    TR_keywords = keywords.keywords(text, scores=True)
    return [kv[0] for kv in TR_keywords[:5]]

class BBCSpider(scrapy.Spider):
    name = "bbc"
    start_urls = [
        home_url
    ]
        
    def parse(self, response):
        if response.url == home_url:
            article_urls = parse_homepage(response)
            for article in article_urls:
                yield scrapy.Request(article, callback=self.parse)
        else:
            url, author, title, content = parse_article(response)
            keywords = suma_extractor(title, content)
            if content:
                yield {
                    'article_url': url,
                    'author': author.replace('By ', ''),
                    'title' : title,
                    'content' : content,
                    'keywords' : keywords
                }

process = CrawlerProcess(settings={
    "FEEDS": {
        "articles.json": {"format": "json"},
    },
})

process.crawl(BBCSpider)
process.start()
