from tech_news import database
from datetime import datetime


# Requisito 7
def search_by_title(title):
    title = database.search_news({"title": {"$regex": title, "$options": "i"}})

    news_list = []

    if title:
        for new in title:
            tuple_list = f"{new['title']}", f"{new['url']}"
            news_list.append(tuple_list)

    return news_list


# Requisito 8
def search_by_date(date):
    try:
        datetime.fromisoformat(date)
    except ValueError:
        raise ValueError("Data inválida")

    news_date_format = datetime.strptime(date, "%Y-%m-%d").strftime(
        "%d/%m/%Y"
    )

    news = database.search_news({"timestamp": {"$regex": news_date_format}})

    news_list = []

    if news:
        for info in news:
            new_info = f"{info['title']}", f"{info['url']}"
            news_list.append(new_info)

    return news_list


# Requisito 9
def search_by_category(category):
    news = database.search_news(
        {"category": {"$regex": category, "$options": "i"}}
    )

    news_list = []

    if news:
        for new in news:
            new_info = f"{new['title']}", f"{new['url']}"
            news_list.append(new_info)

    return news_list
