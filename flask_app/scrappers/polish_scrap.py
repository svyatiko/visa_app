# from news_scraper import NewsScraper
# from visa_centers_scraper import ViseCentersScraper
# from consulates_scraper import ConsulatesScraper
# import requests
# import requests
# from typing import List
# from typing import List
# from base_scraper import BaseScraper
# from base_scraper import BaseScraper
from abc import abstractmethod
import requests
from bs4 import BeautifulSoup
from typing import List


class BaseScraper:

    headers = {"Authorization": "Bearer 5YpTBRikGN59YHwM18CyGr5F43bFuaak9U8FSMEDmb8"}
    url = "https://d2ab400qlgxn2g.cloudfront.net/dev/spaces/xxg4p8gt3sg6/environments/master/entries?"

    def __init__(self, content_type, language, dest_country, country):
        self._content_type = content_type
        self._language = language
        self._dest_country = dest_country
        self._country = country

    @abstractmethod
    def get_json_response(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class ViseCentersScraper(BaseScraper):
    def __init__(self, language, dest_country, country):
        super().__init__("countryLocation", language, dest_country, country)

    def get_json_response(self) -> dict:
        payload = {
            "content_type": self._content_type,
            "fields.title[match]": f"{self._dest_country} > {self._country} > {self._language}",
            "order": "fields.vacName",
            "limit": "200",
        }

        return requests.get(self.url, params=payload, headers=self.headers).json()

    def get_data(self) -> List[dict]:
        items = self.get_json_response()
        visa_centers = [item["fields"] for item in items["items"]]
        cities = [visa_center["vacName"] for visa_center in visa_centers]
        opening_hours = [
            visa_center["openingHoursObject"] for visa_center in visa_centers
        ]
        vacaddresses = [
            visa_center["address"]["content"][0]["content"][0]["value"].strip("{ }")
            for visa_center in visa_centers
        ]
        addresses = self.__get_addresses(vacaddresses)

        centers_data = [
            {
                # 'city': city,
                "ADRESS": address,
                "EMAIL": "appt.polbrest@vfsglobal.com",
                "APPLY_WORKING_HOURS": hours[0]["day"] + ", " + hours[0]["hours"],
                "ISSUE_WORKING_HOURS": hours[1]["day"] + ", " + hours[1]["hours"],
                "PHONE_NUMBER": None,
                # 'country': 'Poland'
            }
            for city, hours, address in zip(cities, opening_hours, addresses)
        ]

        return centers_data

    def __get_addresses(self, vacaddresses: List[str]) -> List[str]:
        payload = {
            "content_type": "resourceGroup",
            "fields.locale": (
                f"vfs&{self._language}&{self._dest_country}&{self._dest_country} "
                f"> {self._language}&{self._dest_country} > {self._country}"
                f"&{self._dest_country} > {self._country} > {self._language}"
            ),
            "limit": 500,
        }

        response = requests.get(self.url, params=payload, headers=self.headers)
        resources = response.json()["items"][4]["fields"]["resources"]
        addresses = [resources[vacaddress] for vacaddress in vacaddresses]
        return addresses


class ConsulatesScraper:
    def __init__(self):
        self.url = "http://catalogpl.by/infa/99-posolstva-i-konsul-stva-polshi.html"

    def get_list_data(self) -> List[List[str]]:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        items = soup.find("div", class_="newsitem_text").find_all("ul")
        consulates = list(map(lambda item: item.text.strip(), items))
        return [embassy.split("\n") for embassy in consulates]

    def parse_data(self):
        consulates = self.get_list_data()
        return [
            {
                "address": consulate[1].split(":", maxsplit=1)[1].strip().rstrip("."),
                "phone": consulate[2]
                .split(":", maxsplit=1)[1]
                .replace(" ", " ")
                .strip()
                .rstrip("."),
                "working hours": consulate[3]
                .split(":", maxsplit=1)[1]
                .strip()
                .rstrip("."),
                "working hours for get a visa": consulate[4]
                .split(":", maxsplit=1)[1]
                .strip()
                .rstrip("."),
                "working hours for delivery of docs": consulate[5]
                .split(":", maxsplit=1)[1]
                .strip()
                .rstrip("."),
            }
            for consulate in consulates
        ]

    def get_data(self) -> List[dict]:
        consulates = self.parse_data()

        return [
            {
                "ADRESS": consulate["address"],
                "EMAIL": None,
                "WORKING_HOURS": consulate["working hours"],
                "PHONE_NUMBER_1": consulate["phone"].split(",")[0],
                "PHONE_NUMBER_2": consulate["phone"].split(",")[1]
                if len(consulate["phone"].split(",")) > 1
                else None,
                # 'country': 'Poland'
            }
            for consulate in consulates
        ]


class NewsScraper(BaseScraper):
    def __init__(self, language, dest_country, country):
        super().__init__("countryNews", language, dest_country, country)

    def get_json_response(self) -> dict:
        payload = {
            "content_type": self._content_type,
            "fields.locale": (
                f"{self._dest_country} > {self._country} > {self._language}"
                f"&{self._dest_country} > {self._language}"
            ),
            "fields.permanent": "true",
        }

        return requests.get(self.url, params=payload, headers=self.headers).json()

    def get_data(self) -> List[dict]:
        data = self.get_json_response()
        all_news = [item["fields"] for item in data["items"]]
        contents = [
            news["intro"]["content"][0]["content"][0]["value"] for news in all_news
        ]
        dates = [news["date"] for news in all_news]
        urls = [
            f"https://visa.vfsglobal.com/{self._country}/{self._language}/{self._dest_country}/news/"
            + news["slug"]
            for news in all_news
        ]

        news_data = [
            {
                "DATE": date,
                "TITLE": content.strip()[:50],
                "BODY": content.strip(),
                "LINK": url,
            }
            for date, content, url in zip(dates, contents, urls)
        ]

        return news_data


class PolishScraper:
    def __init__(self, language="ru", dest_country="pol", country="blr"):
        self.visa_centers = ViseCentersScraper(language, dest_country, country)
        self.news = NewsScraper(language, dest_country, country)
        self.consulates = ConsulatesScraper()

    def get_visa_centers(self):
        return self.visa_centers.get_data()

    def get_news(self):
        return self.news.get_data()

    def get_consulates(self):
        return self.consulates.get_data()

    def get_union_poland_data(self):
        data = {
            "VISAAC": self.get_visa_centers(),
            "CONSULATE": self.get_consulates(),
            "NEWS": self.get_news(),
        }
        return data
