import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
        )
        time.sleep(1)
        if response.status_code == 200:
            return response.text
        return None
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(html_content)

    links = []

    for url in selector.css(".entry-title"):
        link = url.css("a::attr(href)").get()
        links.append(link)

    return links


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_page = selector.css("a.next::attr(href)").get()
    if next_page:
        return next_page
    return None


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)
    dict_news = {}
    dict_news["url"] = selector.css("[rel=canonical]::attr(href)").get()
    dict_news["title"] = selector.css(".entry-title::text").get().strip()
    dict_news["timestamp"] = selector.css(".meta-date::text").get()
    dict_news["writer"] = selector.css(".author a::text").get()
    dict_news["reading_time"] = int(
        selector.css(".meta-reading-time::text").re_first(r"\d+"))

    dict_news["summary"] = "".join(
        selector.css("div.entry-content > p:first-of-type *::text").getall()
    ).strip()
    dict_news["category"] = selector.css(".meta-category .label::text").get()

    return dict_news


# Requisito 5
def get_tech_news(amount):
    url = fetch("https://blog.betrybe.com/")
    links_news = scrape_updates(url)
    list_news = []

    while amount > len(links_news):
        link = scrape_next_page_link(url)
        url = fetch(link)
        links_news.extend(scrape_updates(url))

    for news in links_news:
        url = fetch(news)
        list_news.append(scrape_news(url))

    create_news(list_news[:amount])

    return list_news[:amount]
