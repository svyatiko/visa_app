import json
from bs4 import BeautifulSoup
import requests


def get_info_site(url: str):
    r = requests.get(url)
    return r.text


def collect_info_data(html):
    all_centres = []

    soup = BeautifulSoup(html, "html.parser")

    centers = soup.find_all("table", class_="table")

    for center in centers:

        info = {}

        country_and_type = center.find("th")
        if country_and_type is None:
            break
        country_and_type = country_and_type.text.split(" ")

        parts = center.find_all("div", class_="marginBottom")

        for part in parts:
            rows = part.find_all("div", class_="row")
            if rows[0].text == "Часы работы:":
                info["ISSUE_WORKING_HOURS"] = rows[2].text
                info["APPLY_WORKING_HOURS"] = rows[4].text
                print("r_1", rows[1].text)
                print("r_3", rows[3].text)

            elif rows[0].text == "Адрес":
                address = rows[1].text.replace("\n\t", "")
                info["ADRESS"] = address

            else:
                key = ""
                if rows[0].text == "почта":
                    key = "EMAIL"
                elif rows[0].text == "Тел":
                    key = "PHONE_NUMBER"
                info[key] = rows[1].text
                print("r_0", rows[0].text)

        all_centres.append(info)

    return all_centres


def write_data_to_file(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_visa_center():
    with open("data_spain.json", "r", encoding="utf-8") as file:
        text = json.load(file)
    return text


def get_info_site1(*urls):
    return [requests.get(url).text for url in urls]


def create_correct_data(jsons_data):
    result_data = []

    for json_data in jsons_data:
        data = json.loads(json_data)
        list_of_news = data["data"]["stories"]

        for news in list_of_news:
            date = news["docs"][0]["time"][:10]
            currect_item = {
                "TITLE": "".join([item["text"] for item in news["docs"][0]["title"]]),
                "BODY": "".join([item["text"] for item in news["docs"][0]["text"]]),
                "LINK": news["docs"][0]["url"],
                "DATE": date,
            }

            result_data.append(currect_item)

    return result_data


def get_union_spain_data():
    # visa-centers
    html = get_info_site("https://blsspain-belarus.com/contact.php")
    visaac = collect_info_data(html)

    # news
    inf = get_info_site1(
        "https://newssearch.yandex.ru/news/search?ajax=0&from_archive=1&neo_parent_id=1647441873582156-81607431716702717200156-production-news-app-host-112-NEWS-NEWS_NEWS_SEARCH&p=2&text=испанский+визовый+центр+в+Беларуси"
    )
    news = create_correct_data(inf)

    data = {"visaac": visaac, "consulate": [], "news": news}
    # write_data_to_file(data)
    return data
