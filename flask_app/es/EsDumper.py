from .EsController import EsController


class EsDumper:
    indices = {
        "latvia": {
            "consulate": "latv_cons",
            "visaac": "latv_visaac",
            "news": "latv_news",
        },
        "poland": {"consulate": "pol_cons", "visaac": "pol_visaac", "news": "pol_news"},
        "lithuania": {
            "consulate": "lith_cons",
            "visaac": "lith_visaac",
            "news": "lith_news",
        },
        "thailand": {
            "consulate": "thai_cons",
            "visaac": "thai_visaac",
            "news": "thai_news",
        },
        "spain": {
            "consulate": "spain_cons",
            "visaac": "spain_visaac",
            "news": "spain_news",
        },
    }

    CONSULATE = "consulate"
    VISA_CENTER = "visaac"
    NEWS = "news"

    def __init__(self):
        self.es_controller = EsController()

    def add_consulates(self, consulates, index_name):
        for index, consulate in enumerate(consulates):
            self.es_controller.add_data(
                index_name,
                index + 1,
                {
                    "address": consulate["ADRESS"],
                    "email": consulate["EMAIL"],
                    "telephone1": consulate["PHONE_NUMBER_1"],
                    "telephone2": consulate["PHONE_NUMBER_1"],
                    "worktime": consulate["WORKING_HOURS"],
                },
            )

    def add_visa_centers(self, visa_centers, index_name):
        for index, visa_center in enumerate(visa_centers):
            self.es_controller.add_data(
                index_name,
                index + 1,
                {
                    "address": visa_center["ADRESS"],
                    "email": visa_center["EMAIL"],
                    "issue_worktime": visa_center["ISSUE_WORKING_HOURS"],
                    "apply_worktime": visa_center["APPLY_WORKING_HOURS"],
                    "telephone1": visa_center["PHONE_NUMBER"],
                    "telephone2": "null",
                },
            )

    def add_news(self, news, index_name):
        for index, news_item in enumerate(news):
            self.es_controller.add_data(
                index_name,
                index + 1,
                {
                    "date": news_item["DATE"],
                    "title": news_item["TITLE"],
                    "body": news_item["BODY"],
                    "link": news_item["LINK"],
                },
            )

    def init_indices(self, data, country):
        [
            self.es_controller.delete_index(index)
            for index in [
                EsDumper.indices[country]["consulate"],
                EsDumper.indices[country]["visaac"],
                EsDumper.indices[country]["news"],
            ]
        ]
        self.add_consulates(data["CONSULATE"], EsDumper.indices[country]["consulate"])
        self.add_visa_centers(data["VISAAC"], EsDumper.indices[country]["visaac"])
        self.add_news(data["NEWS"], EsDumper.indices[country]["news"])
